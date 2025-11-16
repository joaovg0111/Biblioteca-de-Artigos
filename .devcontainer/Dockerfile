FROM python:3.12

# Set environment variables for Python.
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH="/home/se/.local/bin:${PATH}"

# Create the 'se' user that devcontainer.json expects
ARG USER=se
ARG UID=1000
ARG GID=1000
RUN groupadd -g ${GID} ${USER} && \
    useradd -m -u ${UID} -g ${GID} -s /bin/bash ${USER}

# Install system-level dependencies.
RUN apt-get update && apt-get install -y --no-install-recommends \
    # --- Database ---
    sqlite3 \
    \
    # --- Version Control ---
    git \
    \
    # --- PDF Export Dependencies ---
    libpango-1.0-0 \
    libcairo2 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    shared-mime-info \
    \
    # --- Email System ---
    msmtp \
    \
    # --- Playwright Dependencies (para testes E2E) ---
    libnspr4 \
    libnss3 \
    libdbus-1-3 \
    libatk1.0-0t64 \
    libatk-bridge2.0-0t64 \
    libatspi2.0-0t64 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libxkbcommon0 \
    libasound2t64 \
    libcups2t64 \
    # Limpa o cache do apt
    && rm -rf /var/lib/apt/lists/*

# Switch to the non-root user.
USER ${USER}

# Workdir must match devcontainer "workspaceFolder"
WORKDIR /home/${USER}/workspace
