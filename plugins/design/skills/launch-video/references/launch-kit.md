# Launch kit: images, post templates, and publishing

## Images

One HTML page built from the video's own components, a variant per size, rendered with
`scripts/shoot_images.cjs`:

| Variant | Size | Use |
|---|---|---|
| YouTube thumbnail | 1280×720 | YouTube |
| Link preview | 1200×630 | X, LinkedIn, Facebook, `og:image` |
| Square post | 1080×1080 | Instagram, Facebook, LinkedIn |
| Vertical cover | 1080×1920 | Reels, TikTok, Shorts; key text inside the middle 1080×1080 |
| End card | 1920×1080 | YouTube end screen, website hero |

View each at real size. One alt text for all.

## Post templates

One section per platform, a main and a short version, written as the brand:

- TikTok / Reels / Shorts: cover text, caption, short variant, pinned comment, few hashtags.
- YouTube: title, description with chapter timestamps from the film's frame times, thumbnail and
  end-screen choice.
- X: main post, short post, a reply carrying the second message.
- Threads, Instagram/Facebook, LinkedIn: a caption each, register rising casual to measured;
  carousel option.
- Forums such as Reddit: no trailer; give guidance on taking part instead.

End the page with the copy rules, each linked to the decision it comes from, derived from the
project's own sources, never carried between projects.

## Publishing

Put the kit where the person asked. GitHub wiki: clone `<repo>.wiki.git`, videos under `media/`,
images under `images/`, one page linked from the home index, commit and push. In a private repo
`raw.githubusercontent.com` links 404 even for the owner: use relative paths (`media/launch/x.mp4`).
Verify the push with `git status -sb` after a fetch; anonymous `curl` cannot see a private wiki.
