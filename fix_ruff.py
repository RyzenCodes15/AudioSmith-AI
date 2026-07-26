import os
filepath = "backend/app/services/audio_service.py"
with open(filepath, 'r') as f:
    c = f.read()
c = c.replace('raise ValidationError(f"File size exceeds maximum allowed ({max_size} bytes).")', 'raise ValidationError(\n                f"File size exceeds maximum allowed ({max_size} bytes)."\n            )')
with open(filepath, 'w') as f:
    f.write(c)
