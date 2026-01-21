# Sprite API Reference

## Base URL
- Management: `https://api.sprites.dev/v1/sprites`
- Per-sprite: `https://api.sprites.dev/v1/sprites/{name}`

## Authentication
`Authorization: Bearer {token}`

Use `sprite api` CLI wrapper for authenticated calls:
```bash
sprite api -s my-sprite /endpoint
sprite api -s my-sprite /endpoint -X POST -d '{"key":"value"}'
```

---

## SPRITES (Management)

### Create
```
POST /v1/sprites
Body: {"name":"my-sprite"}
```

### List
```
GET /v1/sprites
Query: prefix={prefix}
```

### Get
```
GET /v1/sprites/{name}
```

### Update
```
PUT /v1/sprites/{name}
Body: {"url_settings":{"auth":"public"}}
```

### Delete
```
DELETE /v1/sprites/{name}
```

### Sprite Object
```json
{
  "id": "sprite-uuid",
  "name": "my-sprite",
  "organization": "org-slug",
  "status": "running|stopped|suspended|error|failed",
  "url": "https://my-sprite-xyz.sprites.app",
  "url_settings": {"auth": "sprite|public"}
}
```

---

## EXEC

### Execute Command (HTTP)
```
POST /exec?cmd={cmd}&path={path}&stdin={bool}&env={k=v}&dir={dir}
Body: raw stdin bytes
Response: raw stdout bytes
```

### List Sessions
```
GET /exec
```

### Kill Session
```
POST /exec/{session_id}/kill?signal={signal}&timeout={duration}
```

---

## CHECKPOINT

### Create
```
POST /checkpoint
Body: {"comment": "..."}
Response: NDJSON stream
```

### List
```
GET /checkpoints
```

### Get
```
GET /checkpoints/{id}
Response: {"id":"...","create_time":"...","source_id":"...","comment":"..."}
```

### Restore
```
POST /checkpoints/{id}/restore
Response: NDJSON stream
```

### Delete
```
DELETE /checkpoints/{id}
```

---

## POLICY

### Network Policy
```
GET /policy/network
POST /policy/network
Body: {"rules":[{"domain":"*.example.com","action":"allow"},{"include":"defaults"}]}
```

---

## SERVICES

### List
```
GET /services
```

### Get
```
GET /services/{name}
Response: {"name":"web","cmd":"python","args":[...],"http_port":8000,"state":"running"}
```

### Create/Update
```
PUT /services/{name}
Body: {"cmd":"python","args":["-m","http.server","8000"],"needs":["postgres"],"http_port":8000}
```

### Start/Stop
```
POST /services/{name}/start
POST /services/{name}/stop
```

### Delete
```
DELETE /services/{name}
```

### Logs
```
GET /services/{name}/logs?lines={n}&duration={duration}
```

---

## FS (Filesystem)

### Read
```
GET /fs/read?path={path}&workingDir={dir}
Response: raw file bytes
Supports: Range headers
```

### Write
```
PUT /fs/write?path={path}&workingDir={dir}&mode={mode}&mkdir={bool}
Body: raw file bytes
Response: {"path":"...","size":1234,"mode":"0644"}
```

### List
```
GET /fs/list?path={path}&workingDir={dir}
Response: {"path":"...","entries":[{"name":"file.txt","type":"file","size":1234}],"count":5}
```

### Delete
```
DELETE /fs/delete
Body: {"path":"/file","workingDir":"/","recursive":false,"asRoot":false}
```

### Rename
```
POST /fs/rename
Body: {"source":"/old","dest":"/new","workingDir":"/","asRoot":false}
```

### Copy
```
POST /fs/copy
Body: {"source":"/src","dest":"/dst","workingDir":"/","recursive":true,"preserveAttrs":true,"asRoot":false}
```

### Chmod/Chown
```
POST /fs/chmod
Body: {"path":"/file","mode":"0755","recursive":false}

POST /fs/chown
Body: {"path":"/file","uid":1000,"gid":1000,"recursive":false}
```
