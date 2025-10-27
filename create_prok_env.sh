#!/usr/bin/env bash
set -euo pipefail

# file: create_prok_env.sh
ENV_YAML="./environment.yaml"
ENV_NAME="prok-pipeline-env"

# Use mamba if present, else fall back to conda
if command -v mamba >/dev/null 2>&1; then
  SOLVER="mamba"
else
  SOLVER="conda"
fi

echo "Using solver: $SOLVER"

# 1) Create the environment (will install packages fresh into the env)
$SOLVER env create -f "$ENV_YAML" || {
  echo "Create failed — trying to update/create by name..."
  $SOLVER env create -n "$ENV_NAME" -f "$ENV_YAML"
}

# 2) locate env prefix
CONDA_PREFIX=$(conda info --base >/dev/null 2>&1 && python -c "import os,sys;from pathlib import Path; \
p=Path(os.environ.get('CONDA_PREFIX', '')); \
if p: print(p); else: print(os.path.join(os.path.expanduser('~'),'miniconda3','envs','$ENV_NAME'))" 2>/dev/null) || true

# Better robust detection
CONDA_PREFIX=$(conda env list | awk -v name="$ENV_NAME" '$1==name {print $2}')
if [ -z "$CONDA_PREFIX" ]; then
  # fallback: common path
  CONDA_PREFIX="$HOME/miniconda3/envs/$ENV_NAME"
fi

echo "Environment prefix: $CONDA_PREFIX"

# 3) Create activation/deactivation hooks
ACT_DIR="$CONDA_PREFIX/etc/conda/activate.d"
DEACT_DIR="$CONDA_PREFIX/etc/conda/deactivate.d"
mkdir -p "$ACT_DIR" "$DEACT_DIR"

# Activation script: ensure env bin is first, remove $HOME/.local/bin from PATH while active,
# unset PYTHONPATH, set PYTHONNOUSERSITE=1, save old PATH in CONDA_OLD_PATH
cat > "$ACT_DIR/00env_isolate.sh" <<'ACT'
#!/usr/bin/env bash
# Save existing PATH
export CONDA_OLD_PATH="$PATH"

# Prepend this env's bin to PATH (if CONDA_PREFIX set)
if [ -n "${CONDA_PREFIX:-}" ]; then
  # Remove any occurrence of $HOME/.local/bin from PATH to avoid bypass
  FILTERED=$(echo "$CONDA_OLD_PATH" | awk -v RS=: -v ORS=: '$0 != "'"$HOME/.local/bin"'"' | sed 's/:$//')
  # Prepend env bin and keep the rest (but filtered)
  export PATH="$CONDA_PREFIX/bin:$FILTERED"
fi

# Ensure user site-packages are not used
unset PYTHONPATH
export PYTHONNOUSERSITE=1
ACT

chmod +x "$ACT_DIR/00env_isolate.sh"

# Deactivation script: restore old PATH and unset env variables
cat > "$DEACT_DIR/00env_isolate.sh" <<'DEACT'
#!/usr/bin/env bash
# Restore PATH saved on activation
if [ -n "${CONDA_OLD_PATH:-}" ]; then
  export PATH="$CONDA_OLD_PATH"
  unset CONDA_OLD_PATH
fi

# Unset python user site env var
unset PYTHONNOUSERSITE
DEACT

chmod +x "$DEACT_DIR/00env_isolate.sh"

echo "Activation hooks created in:"
echo "  $ACT_DIR/00env_isolate.sh"
echo "  $DEACT_DIR/00env_isolate.sh"

# 4) Final message and quick verification instructions
cat <<EOF

Environment '$ENV_NAME' created. Next steps:

1) Activate it:
   conda activate $ENV_NAME

2) Verify isolation:
   which busco
   which checkm
   python -c "import sys,site; print('ENABLE_USER_SITE=', site.ENABLE_USER_SITE); print('python=', sys.executable)"

   These should point to $CONDA_PREFIX and ENABLE_USER_SITE should be False.

EOF
