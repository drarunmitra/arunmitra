# Content Creation Guide
## Website: arunmitra.com

This guide explains how to add new content to your Hugo Apéro website after the reorganization.

---

## 📁 Website Structure

```
content/
├── about/          → Profile and CV
├── research/       → Research projects and publications
├── training/       → Workshops and training sessions
├── tools/          → APIs, dashboards, and interactive tools
├── blog/           → Technical tutorials and reflections
├── talk/           → Conference presentations and seminars
└── resume/         → Resume/CV sections
```

---

## 🎯 Navigation Menu (In Order)

1. **About** - Your profile
2. **Research** - Research projects
3. **Training** - Workshops and courses
4. **Tools** - APIs and interactive resources
5. **Blog** - Technical posts
6. **Talks** - Presentations
7. **Contact** - Contact form

---

## ✨ Adding New Content

### Method 1: Using Hugo Command (Terminal)

#### Add a Research Project
```bash
hugo new research/your-project-name/index.md
```

#### Add a Workshop/Training
```bash
hugo new training/workshops/workshop-name/index.md
```

#### Add a Blog Post
```bash
hugo new blog/post-title/index.md
```

#### Add a Tool/API
```bash
hugo new tools/tool-name/index.md
```

#### Add a Talk
```bash
hugo new talk/talk-title/index.md
```

### Method 2: Using RStudio blogdown

#### In RStudio Console:

**Add Research Project:**
```r
blogdown::new_content("research/your-project-name/index.md",
                      kind = "research")
```

**Add Workshop:**
```r
blogdown::new_content("training/workshops/workshop-name/index.md",
                      kind = "workshop")
```

**Add Blog Post:**
```r
blogdown::new_content("blog/post-title/index.md",
                      kind = "blog")
```

**Add Tool:**
```r
blogdown::new_content("tools/tool-name/index.md",
                      kind = "tool")
```

### Method 3: Manual Creation

1. Create a new folder in the appropriate section
2. Copy the archetype template from `archetypes/`
3. Rename to `index.md` or `index.Rmd`
4. Edit the content

---

## 📝 Content Templates

### Research Project Template

Location: `archetypes/research.md`

**Key fields:**
- `title`: Project title
- `subtitle`: Brief description
- `excerpt`: Summary for listings
- `date`: Publication/project date
- `categories`: Research, Health Data Science, etc.
- `tags`: Specific topics
- `links`: Publication, Code, Dashboard URLs

**Sections:**
- Background
- Methods
- Key Findings
- Resources
- Citation

### Workshop Template

Location: `archetypes/workshop.md`

**Key fields:**
- `title`: Workshop name
- `date`: Start date/time
- `date_end`: End date/time
- `event`: Event name (e.g., "STP 608, Indian Systems of Medicine")
- `location`: Venue
- `links`: Slides, Materials, Practice API

**Sections:**
- Workshop Overview
- Learning Objectives
- Topics Covered
- Materials
- Audience

### Blog Post Template

Location: `archetypes/blog.md`

**Key fields:**
- `title`: Post title
- `date`: Publication date
- `categories`: Blog categories
- `tags`: Post tags

**Sections:**
- Introduction
- Code Examples
- Conclusion
- References

### Tool/API Template

Location: `archetypes/tool.md`

**Key fields:**
- `title`: Tool/API name
- `excerpt`: Brief description
- `links`: API URL, Code, Documentation

**Sections:**
- Overview
- Features
- Usage examples
- API Endpoints
- Technical Details

---

## 🖼️ Adding Images

### For Individual Posts

1. Place images in the post's directory:
   ```
   research/covid-analysis/
   ├── index.md
   ├── featured.jpg    (shows in listing)
   └── figure1.png
   ```

2. Reference in markdown:
   ```markdown
   ![Description](figure1.png)
   ```

### Featured Images

Name your main image `featured.jpg` or `featured.png` in the post directory.

---

## 🔗 Internal Links

Link to other sections:
```markdown
- [See my research](/research/)
- [Check out this workshop](/training/workshops/r-programming/)
- [View the API](/tools/hrv-analysis/)
```

---

## 📊 Using R in Posts

### Create .Rmd instead of .md

```bash
hugo new research/analysis-project/index.Rmd
```

### Example R Markdown Post

```rmarkdown
---
title: "My Analysis"
author: "Arun Mitra"
date: '2024-11-13'
---

## Analysis

```{r}
library(ggplot2)
library(dplyr)

# Your R code here
ggplot(mtcars, aes(wt, mpg)) +
  geom_point()
```
```

---

## 🚀 Building and Previewing

### In RStudio:

#### Preview site locally:
```r
blogdown::serve_site()
```

#### Stop preview:
```r
blogdown::stop_server()
```

#### Build site:
```r
blogdown::build_site()
```

### In Terminal:

```bash
hugo server -D
```

Open browser to: http://localhost:1313

---

## 🎨 Content Best Practices

### Research Projects
- Include links to publications, code, and data
- Add visualizations and key figures
- Provide context and impact
- Link to related blog posts (methodology)

### Training/Workshops
- Link to all materials (slides, exercises, data)
- Include learning objectives
- Add practice API links when available
- Provide prerequisites

### Blog Posts
- Focus on methodology and tutorials
- Include reproducible code
- Add clear explanations
- Link to related research projects

### Tools/APIs
- Provide clear usage examples
- Link to API documentation
- Include technical details
- Add "Try it out" links

---

## 📁 File Organization

### Recommended Structure

```
content/
├── research/
│   ├── covid-vaccine-inequities/
│   │   ├── index.Rmd
│   │   ├── featured.png
│   │   └── figures/
│   ├── hrv-analysis/
│   │   └── index.md
│   └── caesarean-patterns/
│       └── index.md
├── training/
│   └── workshops/
│       ├── r-programming-aiims/
│       │   └── index.md
│       └── biostatistics-workshop/
│           └── index.md
├── tools/
│   ├── hrv-api/
│   │   └── index.md
│   └── workshop-practice-api/
│       └── index.md
└── blog/
    ├── calculating-rt-in-r/
    │   └── index.Rmd
    └── ggplot2-tips/
        └── index.md
```

---

## ⚙️ Draft vs Published

### Draft Content (Not Visible)
```yaml
---
title: "My Draft Post"
draft: true
---
```

### Published Content
```yaml
---
title: "Published Post"
draft: false
---
```

Or remove the `draft` field entirely.

### Preview Drafts
```r
blogdown::serve_site(draft = TRUE)
```

---

## 🔄 Workflow Example

### Adding a New Research Project

1. **Create content:**
   ```r
   blogdown::new_content("research/tb-outcomes/index.Rmd",
                         kind = "research")
   ```

2. **Edit the file:**
   - Update title, excerpt, date
   - Add publication links
   - Write content with R code chunks
   - Add images to the folder

3. **Preview:**
   ```r
   blogdown::serve_site()
   ```

4. **Review in browser** at http://localhost:1313/research/

5. **Finalize:**
   - Set `draft: false`
   - Commit changes to Git

6. **Deploy:**
   - Push to GitHub
   - Site auto-deploys via Netlify/GitHub Pages

---

## 🐛 Troubleshooting

### Site won't build
- Check YAML frontmatter syntax (proper indentation)
- Ensure all required fields are present
- Look for unclosed quotes or brackets

### Images not showing
- Check file path (case-sensitive)
- Ensure images are in post directory
- Use relative paths, not absolute

### R code not executing
- Use `.Rmd` extension, not `.md`
- Check for R errors in console
- Ensure packages are installed

### Links broken
- Use relative URLs starting with `/`
- Example: `/research/` not `research/`
- Check for typos in paths

---

## 📚 Additional Resources

### Hugo Apéro Documentation
- https://hugo-apero-docs.netlify.app

### Hugo Documentation
- https://gohugo.io/documentation/

### blogdown Book
- https://bookdown.org/yihui/blogdown/

---

## ✅ Quick Reference

| Task | Command |
|------|---------|
| New research | `blogdown::new_content("research/NAME/index.md", kind = "research")` |
| New workshop | `blogdown::new_content("training/workshops/NAME/index.md", kind = "workshop")` |
| New blog | `blogdown::new_content("blog/NAME/index.Rmd", kind = "blog")` |
| New tool | `blogdown::new_content("tools/NAME/index.md", kind = "tool")` |
| Preview site | `blogdown::serve_site()` |
| Stop server | `blogdown::stop_server()` |
| Build site | `blogdown::build_site()` |

---

**Last Updated:** November 2024
**Website:** https://arunmitra.com
**Contact:** For questions about the website structure, refer to this guide or the project documentation.
