# Local Deployment Instructions

To run your website on your local machine, use one of the following methods:

### Method 1: Using Docker (Recommended)

Run this command in your terminal:

```bash
docker compose up
```

Then visit: `http://localhost:8080`

### Method 2: Using Jekyll Directly

1. Install Ruby dependencies:
   ```bash
   bundle install
   ```
2. Run the server:
   ```bash
   bundle exec jekyll serve
   ```
   Then visit: `http://localhost:4000`
