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
    # For SQLite command-line interface and database support.
    sqlite3 \
    \
    # --- Version Control ---
    git \
    \
    # --- PDF Export Dependencies (for libraries like WeasyPrint) ---
    libpango-1.0-0 \
    libcairo2 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    shared-mime-info \
    \
    # --- Email System ---
    # A lightweight SMTP client for sending emails.
    msmtp \
    \
    && rm -rf /var/lib/apt/lists/*

# Switch to the non-root user.
USER ${USER}

# Workdir must match devcontainer "workspaceFolder"
WORKDIR /home/${USER}/workspace
