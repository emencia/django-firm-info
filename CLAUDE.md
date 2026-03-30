# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Setup
make venv       # Create .venv virtualenv
make install    # Install all dev dependencies

# Testing
make test          # Run tests (reuses DB)
make test-initial  # Run tests from clean DB (required after migration changes)

# Single test
.venv/bin/pytest tests/test_models.py::TestFirmContact::test_singleton -v

# Linting
make flake

# Database
make migrate       # Apply migrations
make migrations    # Create new migrations for firm_info

# Dev server
make run           # Start sandbox server at 0.0.0.0:8001

# Docs
make docs          # Build Sphinx HTML docs
make livedocs      # Live-reload docs server

# Release
make quality       # Full check: flake8 + tests + docs + release check
make build-package
make release       # Upload to PyPI
```

## Architecture

This is a reusable Django app (`firm_info/`) with a `sandbox/` demo project used for development and testing.

### Core concept: Singletons

Three models use `SingletonManager` (`firm_info/managers.py`) to enforce a single row per model: `FirmContact`, `SocialSharing`, and `Tracking`. Attempting to create a second instance raises a `ValueError`. The admin (`firm_info/admin.py`) enforces this via `UniqueModelAdmin` which disables the "add" permission once one instance exists.

### Models

- **FirmContact** — Primary model. Stores contact details, logos, descriptions. Has a one-to-many relation to `Link` objects (social network URLs). Uses `SmartMediaField` for images with auto file cleanup on delete/change.
- **Link** — Social media URL entries (16+ platforms), tied to `FirmContact` via FK.
- **SocialSharing** — Singleton for OG metadata (image, description, Twitter site).
- **Tracking** — Singleton for analytics tags.
- **AppsBanner** — One banner per `application_type` (5 choices: `application_sent`, `free_apply`, `job_offers`, `news`, `trombinoscope`).

### Template integration

Template tags in `firm_info/templatetags/firm_info.py` accept a template path and delegate rendering to serializer functions in `firm_info/serializers.py`. Each serializer returns a dict for template context. Usage:

```html
{% load firm_info %}
{% firm_contact "firm_info/firm_contact.html" %}
{% firm_social_links "firm_info/social_links.html" %}
{% app_banner "news" "firm_info/apps_banner.html" %}
```

### Optional integrations

- **CMS editor:** `firm_info/compat/editor_widget.py` tries to import `djangocms-text` or `djangocms-text-ckeditor`; falls back to plain `Textarea`.
- **django-configurations:** `firm_info/contrib/django_configuration.py` provides a mixin class.

### Test setup

Tests use the `sandbox.settings.tests` settings module (in-memory SQLite). Factories are in `firm_info/factories.py`. Fixtures are in `tests/conftest.py`. Test files mirror the module they test (`tests/test_models.py`, `tests/test_serializers.py`, etc.).

### Settings

The only custom setting is `FIRMINFO_APP_NAME` (default: `"Firm information"`), which controls the app label in the Django admin.
