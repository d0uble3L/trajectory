# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in Trajectory, please **do not** open a public GitHub issue. Instead:

1. **Email**: Security issues should be reported privately to michaeltayo@example.com (or use GitHub Security Advisory)
2. **GitHub Security Tab**: Use "Security" → "Report a vulnerability" to create a private advisory
3. **Include**:
   - Description of the vulnerability
   - Affected component(s)
   - Steps to reproduce
   - Potential impact

## Response Timeline

- **Acknowledgment**: We will acknowledge reports within 24 hours
- **Investigation**: We aim to triage within 48 hours
- **Fix**: Critical issues within 7 days, high priority within 14 days
- **Disclosure**: Coordinated responsible disclosure with credit

## Supported Versions

| Version | Supported          |
|---------|-------------------|
| 1.x     | ✓ In development  |

## Security Practices

- All commits are scanned for secrets via TruffleHog
- Dependencies are audited weekly via OWASP Dependency-Check
- Docker images are scanned for vulnerabilities via Trivy & Grype
- Python code is analyzed via Bandit (SAST) and CodeQL
- All PRs require passing security checks before merge

## Dependencies

Third-party security:
- **FastAPI**: Security patches tracked via GitHub security advisories
- **Uvicorn**: Community maintained, updates monitored
- **Pydantic**: Security critical updates applied promptly

## Compliance & Standards

- OWASP Top 10 adherence
- CWE/SANS Top 25 prevention focus
- PCI DSS guidelines for any financial data
