#!/usr/bin/env bash
#
# Pull latest Docker images and recreate running containers.
# Designed for unattended use via crontab on macOS and Linux (incl. Raspberry Pi).
#
# Crontab examples:
#   0 4 * * 0 /home/pi/dotfiles/docker/upgrade-images.sh          # Raspberry Pi
#   0 4 * * 0 /Users/you/dotfiles/docker/upgrade-images.sh          # macOS
#
# Optional: list extra compose project directories (one per line):
#   ~/.config/docker/upgrade-dirs

set -uo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

resolve_home() {
  if [[ -n "${HOME:-}" && -d "$HOME" ]]; then
    return 0
  fi

  local user="${USER:-$(id -un 2>/dev/null || echo "")}"
  if [[ -n "$user" ]] && command -v getent >/dev/null 2>&1; then
    HOME="$(getent passwd "$user" | cut -d: -f6)"
  fi

  if [[ -z "${HOME:-}" || ! -d "$HOME" ]]; then
    local user
    user="$(id -un 2>/dev/null || echo "")"
    if [[ -n "$user" ]]; then
      HOME="$(eval echo "~${user}")"
    fi
  fi

  if [[ -z "${HOME:-}" || ! -d "$HOME" ]]; then
    HOME="/tmp"
  fi

  export HOME
}

resolve_home

readonly LOG_DIR="${LOG_DIR:-${HOME}/.local/log}"
readonly LOG_FILE="${LOG_FILE:-${LOG_DIR}/docker-upgrade.log}"
readonly LOCK_FILE="${LOCK_FILE:-${TMPDIR:-/tmp}/docker-upgrade.lock}"
readonly EXTRA_DIRS_FILE="${EXTRA_DIRS_FILE:-${HOME}/.config/docker/upgrade-dirs}"

# macOS Homebrew + common Linux paths (Raspberry Pi OS, Debian, snap)
export PATH="/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin:${PATH:-}"

COMPOSE_V2=0
COMPOSE_V1=0
COMPOSE_CMD=()

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"
}

log_both() {
  log "$*" | tee -a "$LOG_FILE"
}

detect_compose() {
  if docker compose version >/dev/null 2>&1; then
    COMPOSE_V2=1
  fi
  if command -v docker-compose >/dev/null 2>&1 && docker-compose version >/dev/null 2>&1; then
    COMPOSE_V1=1
  fi

  if ((COMPOSE_V2 == 0 && COMPOSE_V1 == 0)); then
    log_both "ERROR: neither 'docker compose' nor 'docker-compose' found"
    exit 1
  fi
}

compose() {
  if ((COMPOSE_V2 == 1)); then
    docker compose "$@"
  else
    docker-compose "$@"
  fi
}

require_docker() {
  if ! command -v docker >/dev/null 2>&1; then
    log_both "ERROR: docker not found in PATH"
    exit 1
  fi

  if ! docker info >/dev/null 2>&1; then
    log_both "ERROR: docker daemon is not running or not accessible"
    exit 1
  fi

  detect_compose
}

acquire_lock() {
  if command -v flock >/dev/null 2>&1; then
    exec 9>"$LOCK_FILE"
    if ! flock -n 9; then
      log_both "Another upgrade is already running. Exiting."
      exit 0
    fi
    trap 'rm -f "$LOCK_FILE"' EXIT
    return 0
  fi

  # Fallback for macOS and minimal environments without flock
  if [[ -f "$LOCK_FILE" ]]; then
    local lock_pid
    lock_pid="$(cat "$LOCK_FILE" 2>/dev/null || true)"
    if [[ -n "$lock_pid" ]] && kill -0 "$lock_pid" 2>/dev/null; then
      log_both "Another upgrade is already running (pid ${lock_pid}). Exiting."
      exit 0
    fi
  fi

  echo $$ >"$LOCK_FILE"
  trap 'rm -f "$LOCK_FILE"' EXIT
}

find_compose_file() {
  local dir="$1"
  local file

  for file in compose.yml docker-compose.yml docker-compose.yaml; do
    if [[ -f "${dir}/${file}" ]]; then
      echo "${dir}/${file}"
      return 0
    fi
  done

  return 1
}

build_compose_cmd() {
  local project="${1:-}"
  local compose_dir="${2:-}"
  local compose_file=""

  COMPOSE_CMD=()

  if [[ -n "$compose_dir" ]]; then
    compose_file="$(find_compose_file "$compose_dir" || true)"
  fi

  if ((COMPOSE_V2 == 1)); then
    COMPOSE_CMD=(docker compose)
    [[ -n "$project" ]] && COMPOSE_CMD+=(-p "$project")
    [[ -n "$compose_file" ]] && COMPOSE_CMD+=(-f "$compose_file")
  else
    COMPOSE_CMD=(docker-compose)
    [[ -n "$compose_file" ]] && COMPOSE_CMD+=(-f "$compose_file")
    [[ -n "$project" ]] && COMPOSE_CMD+=(-p "$project")
  fi
}

upgrade_compose_project() {
  local project="$1"
  local compose_dir="${2:-}"

  log_both "Upgrading compose project: ${project}"

  build_compose_cmd "$project" "$compose_dir"

  local compose_file=""
  if [[ -n "$compose_dir" ]]; then
    compose_file="$(find_compose_file "$compose_dir" || true)"
  fi

  if [[ -z "$project" && -z "$compose_file" ]]; then
    log_both "ERROR: could not resolve compose file for project ${project}"
    return 1
  fi

  if [[ -n "$compose_dir" && -d "$compose_dir" && COMPOSE_V1 == 1 && COMPOSE_V2 == 0 ]]; then
    if ! (cd "$compose_dir" && "${COMPOSE_CMD[@]}" pull >>"$LOG_FILE" 2>&1); then
      log_both "ERROR: pull failed for project ${project}"
      return 1
    fi
    if ! (cd "$compose_dir" && "${COMPOSE_CMD[@]}" up -d --remove-orphans >>"$LOG_FILE" 2>&1); then
      log_both "ERROR: recreate failed for project ${project}"
      return 1
    fi
  else
    if ! "${COMPOSE_CMD[@]}" pull >>"$LOG_FILE" 2>&1; then
      log_both "ERROR: pull failed for project ${project}"
      return 1
    fi
    if ! "${COMPOSE_CMD[@]}" up -d --remove-orphans >>"$LOG_FILE" 2>&1; then
      log_both "ERROR: recreate failed for project ${project}"
      return 1
    fi
  fi

  log_both "Finished compose project: ${project}"
  return 0
}

upgrade_compose_from_dir() {
  local dir="$1"
  local compose_file

  if [[ ! -d "$dir" ]]; then
    log_both "WARN: compose directory not found: ${dir}"
    return 1
  fi

  compose_file="$(find_compose_file "$dir" || true)"
  if [[ -z "$compose_file" ]]; then
    log_both "WARN: no compose file found in ${dir}"
    return 1
  fi

  log_both "Upgrading compose directory: ${dir}"

  if ((COMPOSE_V1 == 1 && COMPOSE_V2 == 0)); then
    if ! (cd "$dir" && docker-compose -f "$compose_file" pull >>"$LOG_FILE" 2>&1); then
      log_both "ERROR: pull failed for ${dir}"
      return 1
    fi
    if ! (cd "$dir" && docker-compose -f "$compose_file" up -d --remove-orphans >>"$LOG_FILE" 2>&1); then
      log_both "ERROR: recreate failed for ${dir}"
      return 1
    fi
  else
    if ! compose -f "$compose_file" pull >>"$LOG_FILE" 2>&1; then
      log_both "ERROR: pull failed for ${dir}"
      return 1
    fi
    if ! compose -f "$compose_file" up -d --remove-orphans >>"$LOG_FILE" 2>&1; then
      log_both "ERROR: recreate failed for ${dir}"
      return 1
    fi
  fi

  log_both "Finished compose directory: ${dir}"
  return 0
}

list_compose_projects() {
  if ((COMPOSE_V2 == 1)) && compose ls --format '{{.Name}}' >/dev/null 2>&1; then
    compose ls --format '{{.Name}}\t{{.ConfigFiles}}'
    return 0
  fi

  # Fallback for docker-compose v1 and older compose setups (common on Raspberry Pi)
  docker ps --filter "label=com.docker.compose.project" \
    --format '{{.Label "com.docker.compose.project"}}\t{{.Label "com.docker.compose.project.config_files"}}' \
    2>/dev/null | awk -F '\t' '!seen[$1]++ { print }'
}

resolve_compose_dir() {
  local project="$1"
  local config_files="${2:-}"
  local compose_dir=""

  if [[ -n "$config_files" ]]; then
    compose_dir="$(dirname "${config_files%%,*}")"
    [[ -d "$compose_dir" ]] && echo "$compose_dir" && return 0
  fi

  compose_dir="$(docker ps --filter "label=com.docker.compose.project=${project}" \
    --format '{{.Label "com.docker.compose.project.working_dir"}}' 2>/dev/null | head -n 1)"

  if [[ -n "$compose_dir" && -d "$compose_dir" ]]; then
    echo "$compose_dir"
    return 0
  fi

  return 1
}

is_compose_container() {
  local cid="$1"
  local project
  project="$(docker inspect -f '{{index .Config.Labels "com.docker.compose.project"}}' "$cid")"
  [[ -n "$project" ]]
}

recreate_standalone_container() {
  local cid="$1"
  local name image restart

  name="$(docker inspect -f '{{.Name}}' "$cid" | sed 's|^/||')"
  image="$(docker inspect -f '{{.Config.Image}}' "$cid")"
  restart="$(docker inspect -f '{{.HostConfig.RestartPolicy.Name}}' "$cid")"

  log_both "Upgrading standalone container: ${name} (${image})"

  if ! docker pull "$image" >>"$LOG_FILE" 2>&1; then
    log_both "ERROR: pull failed for ${name} (${image})"
    return 1
  fi

  local -a run_args=()
  run_args+=(--name "$name")

  if [[ "$restart" != "no" && -n "$restart" ]]; then
    local restart_max
    restart_max="$(docker inspect -f '{{.HostConfig.RestartPolicy.MaximumRetryCount}}' "$cid")"
    if [[ "$restart" == "on-failure" && "$restart_max" -gt 0 ]]; then
      run_args+=(--restart="${restart}:${restart_max}")
    else
      run_args+=(--restart="$restart")
    fi
  fi

  local hostname
  hostname="$(docker inspect -f '{{.Config.Hostname}}' "$cid")"
  if [[ -n "$hostname" && "$hostname" != "$name" ]]; then
    run_args+=(--hostname "$hostname")
  fi

  local network_mode
  network_mode="$(docker inspect -f '{{.HostConfig.NetworkMode}}' "$cid")"
  if [[ "$network_mode" == "host" || "$network_mode" == "none" ]]; then
    run_args+=(--network "$network_mode")
  elif [[ "$network_mode" != "default" && "$network_mode" != "bridge" ]]; then
    run_args+=(--network "$network_mode")
  fi

  local port_map
  while IFS= read -r port_map; do
    [[ -n "$port_map" ]] && run_args+=(-p "$port_map")
  done < <(docker inspect -f '{{range $p, $conf := .NetworkSettings.Ports}}{{range $conf}}{{if .HostIp}}{{.HostIp}}:{{end}}{{.HostPort}}:{{$p}}{{"\n"}}{{end}}{{end}}' "$cid")

  local mount
  while IFS= read -r mount; do
    [[ -n "$mount" ]] && run_args+=(-v "$mount")
  done < <(docker inspect -f '{{range .Mounts}}{{if eq .Type "volume"}}{{.Name}}:{{.Destination}}{{else}}{{.Source}}:{{.Destination}}{{end}}{{if .Mode}}:{{.Mode}}{{end}}{{"\n"}}{{end}}' "$cid")

  local env_var
  while IFS= read -r env_var; do
    [[ -n "$env_var" ]] && run_args+=(-e "$env_var")
  done < <(docker inspect -f '{{range .Config.Env}}{{println .}}{{end}}' "$cid")

  local label
  while IFS= read -r label; do
    [[ -n "$label" ]] && run_args+=(-l "$label")
  done < <(docker inspect -f '{{range $k, $v := .Config.Labels}}{{$k}}={{$v}}{{"\n"}}{{end}}' "$cid" | grep -Ev '^com\.docker\.' || true)

  local -a cmd=()
  local cmd_line
  while IFS= read -r cmd_line; do
    [[ -n "$cmd_line" ]] && cmd+=("$cmd_line")
  done < <(docker inspect -f '{{range .Config.Cmd}}{{.}}{{"\n"}}{{end}}' "$cid")

  if ! docker stop "$cid" >>"$LOG_FILE" 2>&1; then
    log_both "ERROR: stop failed for ${name}"
    return 1
  fi

  if ! docker rm "$cid" >>"$LOG_FILE" 2>&1; then
    log_both "ERROR: remove failed for ${name}"
    return 1
  fi

  if ((${#cmd[@]} > 0)); then
    if ! docker run -d "${run_args[@]}" "$image" "${cmd[@]}" >>"$LOG_FILE" 2>&1; then
      log_both "ERROR: recreate failed for ${name}"
      return 1
    fi
  else
    if ! docker run -d "${run_args[@]}" "$image" >>"$LOG_FILE" 2>&1; then
      log_both "ERROR: recreate failed for ${name}"
      return 1
    fi
  fi

  log_both "Finished standalone container: ${name}"
  return 0
}

upgrade_running_compose_projects() {
  local failures=0
  local -a seen_projects=()
  local project config_files compose_dir already_seen seen

  while IFS=$'\t' read -r project config_files; do
    [[ -z "$project" ]] && continue

    already_seen=0
    for seen in "${seen_projects[@]:-}"; do
      if [[ "$seen" == "$project" ]]; then
        already_seen=1
        break
      fi
    done
    if ((already_seen)); then
      continue
    fi
    seen_projects+=("$project")

    compose_dir="$(resolve_compose_dir "$project" "$config_files" || true)"

    if ! upgrade_compose_project "$project" "$compose_dir"; then
      failures=$((failures + 1))
    fi
  done < <(list_compose_projects)

  return "$failures"
}

upgrade_extra_compose_dirs() {
  local failures=0
  local dir

  [[ -f "$EXTRA_DIRS_FILE" ]] || return 0

  while IFS= read -r dir || [[ -n "$dir" ]]; do
    dir="${dir%%#*}"
    dir="${dir#"${dir%%[![:space:]]*}"}"
    dir="${dir%"${dir##*[![:space:]]}"}"
    [[ -z "$dir" ]] && continue
    [[ "$dir" == ~* ]] && dir="${dir/#\~/$HOME}"

    if ! upgrade_compose_from_dir "$dir"; then
      failures=$((failures + 1))
    fi
  done <"$EXTRA_DIRS_FILE"

  return "$failures"
}

upgrade_standalone_containers() {
  local failures=0
  local cid

  # Snapshot container IDs first so the list is stable while we recreate
  local -a container_ids=()
  while IFS= read -r cid; do
    [[ -n "$cid" ]] && container_ids+=("$cid")
  done < <(docker ps -q 2>/dev/null || true)

  for cid in "${container_ids[@]:-}"; do
    if is_compose_container "$cid"; then
      continue
    fi
    if ! recreate_standalone_container "$cid"; then
      failures=$((failures + 1))
    fi
  done

  return "$failures"
}

prune_old_images() {
  log_both "Pruning dangling images"
  docker image prune -f >>"$LOG_FILE" 2>&1 || log_both "WARN: image prune failed"
}

main() {
  local failures=0
  local step_failures=0

  mkdir -p "$LOG_DIR"
  require_docker
  acquire_lock

  log "=== Docker upgrade started ===" >>"$LOG_FILE"

  upgrade_running_compose_projects
  step_failures=$?
  failures=$((failures + step_failures))

  upgrade_extra_compose_dirs
  step_failures=$?
  failures=$((failures + step_failures))

  upgrade_standalone_containers
  step_failures=$?
  failures=$((failures + step_failures))

  prune_old_images

  if ((failures > 0)); then
    log_both "=== Docker upgrade finished with ${failures} error(s) ==="
  else
    log_both "=== Docker upgrade finished successfully ==="
  fi

  exit "$failures"
}

main "$@"
