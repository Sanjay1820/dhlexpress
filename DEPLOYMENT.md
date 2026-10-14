# GitHub source and Vercel homepage preview

The repository contains the complete website, all service/location pages, original backups, PHP handlers, design assets and maintenance scripts.

Vercel publishes only `dist/index.html` and its referenced CSS, JavaScript, images and fonts. Other source HTML, PHP, backups and Python scripts do not enter the deployment output.

## Vercel

Import `Sanjay1820/dhlexpress`. Keep the repository root as the Root Directory. The checked-in `vercel.json` selects Framework **Other**, Build Command **npm run build** and Output Directory **dist**. No environment variables or dependencies are needed.

The generated homepage sends internal navigation to homepage sections. The repository's original pages and navigation stay intact. In the static preview, submitting an enquiry opens the visitor's email app; the existing PHP handlers remain in the full source for a PHP-capable host.

To build locally with Node.js 20 or later:

```sh
npm run build
```

Generated files, local caches, logs, credentials and Vercel account metadata are ignored by Git.
