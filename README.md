# water-agent
Hourly drink-water reminder posted to a Google Chat space via incoming webhook.
Runs on GitHub Actions, **Mon–Fri, every hour from 08:00 to 17:00 ICT** (UTC+7).

## Setup

1. **Push this repo to GitHub.**
2. Go to **Settings → Secrets and variables → Actions → New repository secret** and add:
   - Name: `GCHAT_WEBHOOK`
   - Value: the full incoming-webhook URL for the Google Chat space (the `chat.googleapis.com/v1/spaces/.../messages?key=...&token=...` link).
3. The schedule is already wired up in `.github/workflows/water-reminder.yml`. To send a test message immediately, open the **Actions** tab, pick **Water reminder**, and click **Run workflow**.

## Schedule

`cron: "0 1-10 * * 1-5"` — top of every hour, 01:00–10:00 UTC, Mon–Fri.
That maps to 08:00–17:00 ICT, i.e. 10 reminders per workday.

GitHub Actions cron is best-effort and can be delayed by a few minutes under load.

## Running locally

```powershell
$env:GCHAT_WEBHOOK = "https://chat.googleapis.com/v1/spaces/.../messages?key=...&token=..."
python water_reminder.py
```

Requires Python 3.12+ (uses only the standard library).

## Customizing messages

Edit the `MESSAGES` list in `water_reminder.py`. Each entry uses `{mention}` as the placeholder for the space-wide `<users/all>` ping. Google Chat plain-text formatting works: `*bold*`, `_italic_`, `~strike~`, `` `mono` ``, and Unicode emoji.
