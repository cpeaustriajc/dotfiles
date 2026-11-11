# QuickTime (macOS)

QuickTime keeps showing the old file when the same path is reopened. Close its documents first,
and give the person this line to reopen a render:

```sh
osascript -e 'tell application "QuickTime Player" to close every document' && open -a "QuickTime Player" <file>
```
