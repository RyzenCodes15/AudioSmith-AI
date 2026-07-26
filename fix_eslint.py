import os
import re

def replace_in_file(filepath, replacements):
    if not os.path.exists(filepath):
        print(f"Not found: {filepath}")
        return
    with open(filepath, 'r') as f:
        content = f.read()
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
        else:
            print(f"Warning: could not find '{old}' in {filepath}")
    with open(filepath, 'w') as f:
        f.write(content)

replace_in_file("frontend/src/app/page.tsx", [
    (
        '[...Array(24)].map((_, i) => (\n                    <div key={i} className={styles.waveBar} style={{ height: `${20 + Math.random() * 60}%` }} />\n                  ))',
        '[45, 60, 35, 70, 25, 80, 50, 40, 65, 30, 55, 75, 45, 60, 35, 70, 25, 80, 50, 40, 65, 30, 55, 75].map((h, i) => (\n                    <div key={i} className={styles.waveBar} style={{ height: `${h}%` }} />\n                  ))'
    ),
    (
        '{Array.from({ length: 24 }).map((_, i) => (\n                    <div key={i} className={styles.waveBar} style={{ height: `${20 + Math.random() * 60}%` }} />\n                  ))}',
        '{[45, 60, 35, 70, 25, 80, 50, 40, 65, 30, 55, 75, 45, 60, 35, 70, 25, 80, 50, 40, 65, 30, 55, 75].map((h, i) => (\n                    <div key={i} className={styles.waveBar} style={{ height: `${h}%` }} />\n                  ))}'
    ),
    (
        '{Array.from({ length: 24 }).map((_, i) => (\n                    <div key={i} className={styles.waveBarClean} style={{ height: `${10 + Math.random() * 30}%` }} />\n                  ))}',
        '{[20, 25, 15, 30, 10, 35, 20, 15, 25, 10, 20, 30, 20, 25, 15, 30, 10, 35, 20, 15, 25, 10, 20, 30].map((h, i) => (\n                    <div key={i} className={styles.waveBarClean} style={{ height: `${h}%` }} />\n                  ))}'
    )
])

replace_in_file("frontend/src/components/auth/LoginForm.tsx", [
    (
        '} catch (err: any) {\n      setError(err.message || \'Invalid credentials. Please try again.\');\n    }',
        '} catch (err: unknown) {\n      setError(err instanceof Error ? err.message : \'Invalid credentials. Please try again.\');\n    }'
    ),
    (
        "Don't have an account?",
        "Don&apos;t have an account?"
    )
])

replace_in_file("frontend/src/components/auth/RegisterForm.tsx", [
    (
        '} catch (err: any) {\n      setError(err.message || \'Registration failed. Please try again.\');\n    }',
        '} catch (err: unknown) {\n      setError(err instanceof Error ? err.message : \'Registration failed. Please try again.\');\n    }'
    )
])

replace_in_file("frontend/src/components/dashboard/UploadSection.tsx", [
    (
        '} catch (err: any) {\n      setError(err.message || \'Failed to upload file.\');\n    }',
        '} catch (err: unknown) {\n      setError(err instanceof Error ? err.message : \'Failed to upload file.\');\n    }'
    ),
    (
        '} catch (err: any) {\n      setError(err.message || \'Failed to upload sample file.\');\n    }',
        '} catch (err: unknown) {\n      setError(err instanceof Error ? err.message : \'Failed to upload sample file.\');\n    }'
    )
])

replace_in_file("frontend/src/lib/api/client.ts", [
    (
        'catch (e: any)',
        'catch (e: unknown)'
    ),
    (
        'catch (e)',
        'catch (_e)'
    )
])

replace_in_file("frontend/src/app/results/[id]/page.tsx", [
    (
        'catch (e) {',
        'catch (_e) {'
    )
])

replace_in_file("frontend/src/components/dashboard/ProcessingHistory.tsx", [
    (
        'catch (e) {',
        'catch (_e) {'
    ),
    (
        'catch (err) {',
        'catch (_err) {'
    )
])
