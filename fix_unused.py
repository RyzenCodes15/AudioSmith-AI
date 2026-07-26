import os

def replace_in_file(filepath, replacements):
    with open(filepath, 'r') as f:
        content = f.read()
    for old, new in replacements:
        content = content.replace(old, new)
    with open(filepath, 'w') as f:
        f.write(content)

replace_in_file("frontend/src/app/results/[id]/page.tsx", [("catch (_e) {", "catch {")])
replace_in_file("frontend/src/components/dashboard/ProcessingHistory.tsx", [
    ("catch (_err) {", "catch {"),
    ("catch (_e) {", "catch {")
])
replace_in_file("frontend/src/lib/api/client.ts", [("catch (_e) {", "catch {")])
