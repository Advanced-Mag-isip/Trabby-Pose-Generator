# Trabby Pose Webapp - Backend API Documentation

## Overview

The Trabby Pose Webapp backend provides a RESTful API for managing puppet assets, preset poses, and facial expressions. Built with Django REST Framework, it's designed for rapid MVP development with extensibility for future features like user-saved poses and complex animations.

---

## Architecture Overview

### Core Data Model

```
PuppetPart (Asset Layer)
├── name: string (e.g., "head-1", "Round Eyes")
├── asset_url: string (path to SVG/image)
├── category: CHOICES [Head, Limbs, Torso, Accessories]
├── subcategory: string (e.g., "Face", "Eyes", "Left Upper Arm", "Torso Shape")
├── order: integer (display order within subcategory)
└── description: text

PosePreset (Template Layout)
├── name: string (e.g., "Thumbs Up", "Happy")
├── slug: unique string (e.g., "thumbs-up")
├── is_expression: boolean (True = facial, False = body pose)
├── description: text
└── part_configurations: [PartConfiguration]

PartConfiguration (Junction Table)
├── pose_preset: ForeignKey
├── puppet_part: ForeignKey
├── position_x, position_y: float (coordinates)
├── rotation: float (0-360 degrees)
├── z_index: integer (layering)
└── scale: float (sizing)
```

### Key Design Principles

1. **Separation of Concerns**: Assets (parts) are decoupled from layouts (poses)
2. **Extensibility**: Easy to add custom poses, expressions, or assets
3. **Clean JSON**: Predictable API responses for frontend consumption
4. **Type Safety**: Full type hints throughout for maintainability

---

## API Endpoints

### Base URL
```
http://localhost:8000/api/
```

### 1. List Body Poses

**Endpoint**: `GET /api/poses/`

**Description**: Retrieve all available body poses (non-expression presets).

**Response (200 OK)**:
```json
{
  "count": 3,
  "data": [
    {
      "id": 1,
      "name": "Neutral",
      "slug": "neutral",
      "description": "Character standing in neutral pose with arms at sides",
      "type": "body_pose",
      "is_expression": false,
      "part_count": 6,
      "created_at": "2026-05-29T10:30:00Z"
    },
    {
      "id": 2,
      "name": "Thumbs Up",
      "slug": "thumbs-up",
      "description": "Character giving enthusiastic thumbs up with right hand",
      "type": "body_pose",
      "is_expression": false,
      "part_count": 7,
      "created_at": "2026-05-29T10:30:00Z"
    },
    {
      "id": 3,
      "name": "Pointing",
      "slug": "pointing",
      "description": "Character pointing forward with right hand",
      "type": "body_pose",
      "is_expression": false,
      "part_count": 7,
      "created_at": "2026-05-29T10:30:00Z"
    }
  ]
}
```

---

### 2. Get Detailed Pose Configuration

**Endpoint**: `GET /api/poses/<slug>/`

**Parameters**:
- `slug` (path): Unique pose identifier (e.g., `thumbs-up`)

**Description**: Retrieve complete pose configuration with all puppet parts, positions, rotations, and z-indices.

**Response (200 OK)**:
```json
{
  "id": 2,
  "name": "Thumbs Up",
  "slug": "thumbs-up",
  "description": "Character giving enthusiastic thumbs up with right hand",
  "type": "body_pose",
  "is_expression": false,
  "part_configurations": [
    {
      "id": 1,
      "puppet_part": {
        "id": 1,
        "name": "head-1",
        "asset_url": "/assets/trabby/sprites/head-1.svg",
        "category": "Head",
        "subcategory": "Head Position",
        "order": 0,
        "description": "A friendly round head for Trabby",
        "created_at": "2026-05-29T10:30:00Z",
        "updated_at": "2026-05-29T10:30:00Z"
      },
      "position_x": 200.0,
      "position_y": 100.0,
      "rotation": 0.0,
      "z_index": 5,
      "scale": 1.0,
      "created_at": "2026-05-29T10:30:00Z",
      "updated_at": "2026-05-29T10:30:00Z"
    },
    {
      "id": 2,
      "puppet_part": {
        "id": 3,
        "name": "torso-standard",
        "asset_url": "/assets/trabby/sprites/torso-standard.svg",
        "category": "Torso",
        "subcategory": "Torso Shape",
        "order": 0,
        "description": "Standard rectangular torso",
        "created_at": "2026-05-29T10:30:00Z",
        "updated_at": "2026-05-29T10:30:00Z"
      },
      "position_x": 200.0,
      "position_y": 180.0,
      "rotation": 0.0,
      "z_index": 4,
      "scale": 1.0,
      "created_at": "2026-05-29T10:30:00Z",
      "updated_at": "2026-05-29T10:30:00Z"
    },
    // ... more part configurations ...
    {
      "id": 5,
      "puppet_part": {
        "id": 19,
        "name": "right-hand-thumbs-up",
        "asset_url": "/assets/trabby/sprites/right-hand-thumbs-up.svg",
        "category": "Accessories",
        "subcategory": "Holdables",
        "order": 0,
        "description": "Hand giving thumbs up gesture",
        "created_at": "2026-05-29T10:30:00Z",
        "updated_at": "2026-05-29T10:30:00Z"
      },
      "position_x": 250.0,
      "position_y": 80.0,
      "rotation": 0.0,
      "z_index": 2,
      "scale": 1.0,
      "created_at": "2026-05-29T10:30:00Z",
      "updated_at": "2026-05-29T10:30:00Z"
    }
  ],
  "created_at": "2026-05-29T10:30:00Z",
  "updated_at": "2026-05-29T10:30:00Z"
}
```

**Error Response (404 Not Found)**:
```json
{
  "detail": "Requested pose not found."
}
```

---

### 3. List Facial Expressions

**Endpoint**: `GET /api/expressions/`

**Description**: Retrieve all available facial expressions.

**Response (200 OK)**:
```json
{
  "count": 3,
  "data": [
    {
      "id": 2,
      "name": "Happy",
      "slug": "happy",
      "description": "Cheerful facial expression with smile",
      "type": "expression",
      "is_expression": true,
      "part_count": 2,
      "created_at": "2026-05-29T10:30:00Z"
    },
    {
      "id": 3,
      "name": "Surprised",
      "slug": "surprised",
      "description": "Shocked or amazed facial expression",
      "type": "expression",
      "is_expression": true,
      "part_count": 2,
      "created_at": "2026-05-29T10:30:00Z"
    },
    {
      "id": 4,
      "name": "Confident",
      "slug": "confident",
      "description": "Determined and confident facial expression",
      "type": "expression",
      "is_expression": true,
      "part_count": 2,
      "created_at": "2026-05-29T10:30:00Z"
    }
  ]
}
```

---

### 4. Get Detailed Expression Configuration

**Endpoint**: `GET /api/expressions/<slug>/`

**Parameters**:
- `slug` (path): Unique expression identifier (e.g., `happy`)

**Description**: Retrieve complete expression configuration with all face elements and their positioning.

**Response**: Same structure as pose detail endpoint, but with `is_expression: true` and face elements instead of body parts.

---

### 5. List Puppet Parts (Asset Inventory)

**Endpoint**: `GET /api/puppet-parts/`

**Query Parameters** (optional):
- `format`: Response format - `hierarchical` (default) or `flat`
- `category`: Filter by category (Head, Limbs, Torso, Accessories)
- `subcategory`: Filter by subcategory (e.g., Face, Eyes, Left Upper Arm)

**Description**: Retrieve all available puppet parts/assets organized hierarchically. Default response groups parts by category and subcategory for easy frontend consumption.

**Response (200 OK) - Hierarchical Format (Default)**:
```json
{
  "Head": {
    "subcategories": ["Head Position", "Face", "Eyes", "Mouth", "Ears", "Hair", "Eyebrows"],
    "options": {
      "Face": [
        {
          "id": 1,
          "name": "head-face-round",
          "asset_url": "/assets/trabby/sprites/head-face-round.svg",
          "description": "A friendly round face for Trabby",
          "order": 0
        },
        {
          "id": 2,
          "name": "head-face-square",
          "asset_url": "/assets/trabby/sprites/head-face-square.svg",
          "description": "A bold square-shaped face",
          "order": 1
        }
      ],
      "Eyes": [
        {
          "id": 3,
          "name": "eyes-neutral",
          "asset_url": "/assets/trabby/sprites/eyes-neutral.svg",
          "description": "Neutral expression eyes",
          "order": 0
        },
        {
          "id": 4,
          "name": "eyes-happy",
          "asset_url": "/assets/trabby/sprites/eyes-happy.svg",
          "description": "Happy expression eyes",
          "order": 1
        }
      ]
    }
  },
  "Limbs": {
    "subcategories": ["Limbs", "Left Upper Arm", "Right Upper Arm", ...],
    "options": {...}
  },
  "Torso": {
    "subcategories": ["Torso Shape"],
    "options": {...}
  },
  "Accessories": {
    "subcategories": ["Wearables", "Holdables"],
    "options": {...}
  }
}
```

**Response (200 OK) - Flat Format**:
```json
{
  "count": 150,
  "data": [
    {
      "id": 1,
      "name": "head-face-round",
      "asset_url": "/assets/trabby/sprites/head-face-round.svg",
      "category": "Head",
      "subcategory": "Face",
      "order": 0,
      "description": "A friendly round face for Trabby",
      "created_at": "2026-05-29T10:30:00Z",
      "updated_at": "2026-05-29T10:30:00Z"
    },
    {
      "id": 2,
      "name": "head-face-square",
      "asset_url": "/assets/trabby/sprites/head-face-square.svg",
      "category": "Head",
      "subcategory": "Face",
      "order": 1,
      "description": "A bold square-shaped face",
      "created_at": "2026-05-29T10:30:00Z",
      "updated_at": "2026-05-29T10:30:00Z"
    }
  ]
}
```

**Filtered Response** (`GET /api/puppet-parts/?category=Limbs&subcategory=Left%20Upper%20Arm&format=flat`):
```json
{
  "count": 5,
  "data": [
    {
      "id": 25,
      "name": "left-upper-arm-neutral",
      "asset_url": "/assets/trabby/sprites/left-upper-arm-neutral.svg",
      "category": "Limbs",
      "subcategory": "Left Upper Arm",
      "order": 0,
      "description": "Left upper arm in neutral position",
      "created_at": "2026-05-29T10:30:00Z",
      "updated_at": "2026-05-29T10:30:00Z"
    },
    {
      "id": 26,
      "name": "left-upper-arm-up",
      "asset_url": "/assets/trabby/sprites/left-upper-arm-up.svg",
      "category": "Limbs",
      "subcategory": "Left Upper Arm",
      "order": 1,
      "description": "Left upper arm raised upward",
      "created_at": "2026-05-29T10:30:00Z",
      "updated_at": "2026-05-29T10:30:00Z"
    }
  ]
}
```

### 6. Get Puppet Parts (Hierarchical Endpoint)

**Endpoint**: `GET /api/puppet-parts/hierarchical/`

**Query Parameters** (optional):
- `category`: Filter by category (Head, Limbs, Torso, Accessories)

**Description**: Dedicated endpoint for fetching puppet parts in hierarchical format. Equivalent to `GET /api/puppet-parts/?format=hierarchical`.

**Response**: Same as hierarchical format shown in endpoint #5 above.

---

## Setup & Database Seeding

### Prerequisites
- Python 3.11+
- Django 5.x
- PostgreSQL (recommended) or SQLite
- Django REST Framework

### Installation

1. **Install dependencies**:
```bash
cd TrabbyPose/backend
pip install -r requirements.txt
```

2. **Configure database** (create `.env` file):
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=postgresql://user:password@localhost:5432/trabby_pose
```

3. **Run migrations**:
```bash
python manage.py migrate
```

4. **Seed initial data**:
```bash
python manage.py seed_assets
```

This will create:
- 150+ puppet parts organized hierarchically:
  - **Head**: 7 subcategories (Head Position, Face, Eyes, Mouth, Ears, Hair, Eyebrows) with ~45 options
  - **Limbs**: 10 subcategories (Limbs, Left Upper Arm, Right Upper Arm, Left Forearm & Hand, Right Forearm & Hand, Left Thigh, Right Thigh, Left Lower Leg & Foot, Right Lower Leg & Foot, Tail) with ~65 options
  - **Torso**: 1 subcategory (Torso Shape) with 7 options
  - **Accessories**: 2 subcategories (Wearables, Holdables) with ~20 options
- 3 body poses (neutral, thumbs-up, pointing)
- 3 facial expressions (happy, surprised, confident)

**To clear and reseed** (destructive):
```bash
python manage.py seed_assets --clear
```

### Verify Installation

```bash
python manage.py shell
>>> from api.models import PosePreset, PuppetPart
>>> PosePreset.objects.count()  # Should return 6
6
>>> PuppetPart.objects.count()  # Should return 150+
153
>>> PuppetPart.objects.values('category').distinct()
<QuerySet [{'category': 'Head'}, {'category': 'Limbs'}, {'category': 'Torso'}, {'category': 'Accessories'}]>
```

---

## Frontend Integration Examples

### React/Astro Component: Fetch Hierarchical Puppet Parts

```javascript
// Fetch hierarchical puppet parts
const response = await fetch('/api/puppet-parts/');
const hierarchy = await response.json();

// Build part picker UI
Object.entries(hierarchy).forEach(([category, categoryData]) => {
  console.log(`Category: ${category}`);
  
  categoryData.subcategories.forEach(subcategory => {
    console.log(`  Subcategory: ${subcategory}`);
    
    categoryData.options[subcategory].forEach(part => {
      console.log(`    - ${part.name}: ${part.asset_url}`);
    });
  });
});
```

### React/Astro Component: Fetch and Render a Pose

```javascript
// Fetch pose data
const response = await fetch('/api/poses/thumbs-up/');
const pose = await response.json();

// Render parts in order of z-index
const sortedParts = pose.part_configurations
  .sort((a, b) => a.z_index - b.z_index);

sortedParts.forEach(config => {
  const { puppet_part, position_x, position_y, rotation, z_index, scale } = config;
  
  // Create SVG element
  const img = document.createElement('img');
  img.src = puppet_part.asset_url;
  img.style.position = 'absolute';
  img.style.left = position_x + 'px';
  img.style.top = position_y + 'px';
  img.style.transform = `rotate(${rotation}deg) scale(${scale})`;
  img.style.zIndex = z_index;
  
  container.appendChild(img);
});
```

### Switching Poses and Expressions

```javascript
// Swap body pose
async function setPose(slug) {
  const poseData = await fetch(`/api/poses/${slug}/`).then(r => r.json());
  renderPose(poseData);
}

// Layer on an expression (overlay face elements)
async function setExpression(slug) {
  const exprData = await fetch(`/api/expressions/${slug}/`).then(r => r.json());
  renderExpression(exprData);  // Higher z-index
}
```

---

## Error Handling

All endpoints follow RESTful conventions:

| Status | Scenario |
|--------|----------|
| 200    | Successful GET request |
| 201    | Successful resource creation |
| 400    | Invalid input/validation error |
| 404    | Resource not found (e.g., invalid slug) |
| 500    | Server error |

**Example Error Response**:
```json
{
  "detail": "Requested pose not found."
}
```

---

## Django Admin Interface

Access the admin panel at `http://localhost:8000/admin/`

### Manage Models
- **Puppet Parts**: Add/edit/delete assets with preview links
- **Pose Presets**: Create poses with inline part configuration editor
- **Part Configurations**: Adjust positioning, rotation, z-index, and scale

---

## Extensibility & Future Enhancements

### Custom User Poses
To enable users to save custom poses:
1. Add `User` FK to `PosePreset`
2. Add `is_public` flag for community poses
3. Add permission checks in view layer

### Animation Frames
To support animations:
1. Create `PoseFrame` model with timestamp/order
2. Create `AnimationSequence` with multiple frames
3. Add endpoints for animation playback

### Constraints & Physics
Future constraint system:
1. Create `PartConstraint` model (e.g., "keep elbow connected to torso")
2. Validate configurations before saving
3. Provide constraint suggestions in frontend

---

## Development Notes

### Type Hints
All Python code uses type hints for clarity and IDE support:
```python
def get_poses_list(request: Request) -> Response:
    poses: List[PosePreset] = PosePreset.objects.filter(...)
    serializer: PosePresetListSerializer = PosePresetListSerializer(poses, many=True)
    return Response(serializer.data)
```

### Testing
Create tests in `api/tests.py`:
```bash
python manage.py test api
```

### Performance
- Uses `prefetch_related` to avoid N+1 queries
- Leverages database indexing on `slug` field
- Consider caching for frequently accessed poses

---

## Support & Questions

For questions about:
- **API Design**: See architecture overview and endpoint documentation
- **Database**: Check models.py for schema
- **Frontend Integration**: See Frontend Integration Examples
- **Deployment**: Refer to Django deployment guides

---

**Last Updated**: May 30, 2026  
**Version**: 1.1.0 (Hierarchical API Redesign)
