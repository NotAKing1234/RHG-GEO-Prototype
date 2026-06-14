import fs from "node:fs/promises";
import path from "node:path";

const [url, outputDir] = process.argv.slice(2);

if (!url || !outputDir) {
  console.error("Usage: node capture.mjs <url> <outputDir>");
  process.exit(2);
}

async function main() {
  const { chromium } = await import("playwright");
  await fs.mkdir(outputDir, { recursive: true });
  const screenshotPath = path.join(outputDir, "screenshot.png");
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const warnings = [];

  try {
    const response = await page.goto(url, { waitUntil: "domcontentloaded", timeout: 30000 });
    await page.waitForTimeout(1200);
    const status = response ? `HTTP ${response.status()}` : "No response";
    const data = await page.evaluate(() => {
      const text = (node) => (node?.textContent || "").replace(/\s+/g, " ").trim();
      const attr = (selector, name) => document.querySelector(selector)?.getAttribute(name) || "";
      const metadata = {
        title: document.title || "",
        description: attr('meta[name="description"]', "content"),
        canonical: attr('link[rel="canonical"]', "href"),
        ogTitle: attr('meta[property="og:title"]', "content"),
        ogDescription: attr('meta[property="og:description"]', "content"),
        robots: attr('meta[name="robots"]', "content"),
      };
      const headings = Array.from(document.querySelectorAll("h1, h2, h3"))
        .slice(0, 80)
        .map((el) => ({
          selector: selectorFor(el),
          tag: el.tagName.toLowerCase(),
          text: text(el),
        }))
        .filter((item) => item.text);
      const sections = Array.from(document.querySelectorAll("main, section, article, header, [role='main'], [data-testid], [class]"))
        .slice(0, 120)
        .map((el) => {
          const label = text(el.querySelector("h1, h2, h3")) || text(el).slice(0, 160);
          return {
            selector: selectorFor(el),
            label,
            tag: el.tagName.toLowerCase(),
            text: text(el).slice(0, 900),
          };
        })
        .filter((item) => item.label && item.text.length > 20);
      const selectorCandidates = [...headings, ...sections.slice(0, 40)].map((item) => ({
        selector: item.selector,
        label: item.text || item.label,
        type: item.tag,
      }));
      return {
        metadata,
        headings,
        sections,
        selector_candidates: selectorCandidates,
        dom_snapshot: document.documentElement.outerHTML.slice(0, 250000),
      };

      function selectorFor(el) {
        if (!el) return "";
        if (el.id) return `#${CSS.escape(el.id)}`;
        const testId = el.getAttribute("data-testid");
        if (testId) return `[data-testid="${CSS.escape(testId)}"]`;
        const parts = [];
        let node = el;
        while (node && node.nodeType === Node.ELEMENT_NODE && parts.length < 5) {
          let part = node.tagName.toLowerCase();
          const classNames = Array.from(node.classList || [])
            .filter(Boolean)
            .slice(0, 2);
          if (classNames.length) part += `.${classNames.map((name) => CSS.escape(name)).join(".")}`;
          const parent = node.parentElement;
          if (parent) {
            const siblings = Array.from(parent.children).filter((child) => child.tagName === node.tagName);
            if (siblings.length > 1) part += `:nth-of-type(${siblings.indexOf(node) + 1})`;
          }
          parts.unshift(part);
          node = parent;
        }
        return parts.join(" > ");
      }
    });
    const finalUrl = page.url();
    await page.screenshot({ path: screenshotPath, fullPage: false });
    await fs.writeFile(path.join(outputDir, "dom_snapshot.html"), data.dom_snapshot, "utf8");
    await browser.close();
    console.log(
      JSON.stringify({
        status,
        source_url: url,
        final_url: finalUrl,
        screenshot_path: screenshotPath,
        metadata: data.metadata,
        headings: data.headings,
        sections: data.sections,
        selector_candidates: data.selector_candidates,
        dom_snapshot_path: path.join(outputDir, "dom_snapshot.html"),
        warnings,
      })
    );
  } catch (error) {
    await browser.close();
    console.error(error?.stack || String(error));
    process.exit(1);
  }
}

main().catch((error) => {
  console.error(error?.stack || String(error));
  process.exit(1);
});
