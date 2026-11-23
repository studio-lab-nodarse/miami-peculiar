// Miami Peculiar trial-box page. One template, two languages: / (EN) and /es/ (ES).
import fs from "node:fs";

// Page values: GitHub repo Variables in CI, a git-ignored .env locally. Real
// environment variables win over the file. Only src/_data/trial.js reads them.
if (fs.existsSync(".env")) process.loadEnvFile(".env");

export default function (eleventyConfig) {
  for (const p of ["assets", ".nojekyll", "robots.txt", "sitemap.xml", "404.html"]) {
    eleventyConfig.addPassthroughCopy({ [p]: p });
  }
  return {
    dir: { input: "src", includes: "_includes", data: "_data", output: "_site" },
    htmlTemplateEngine: "njk",
    templateFormats: ["njk"],
  };
}
