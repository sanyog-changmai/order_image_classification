# Delivery Image Inspection Service

This Django REST API allows clients to upload an image along with an `order_id` to determine whether the image depicts delivered items, using OpenAI's CLIP model for image-text matching.

## Deployment Doc
[Deployment Doc](https://docs.google.com/document/d/1NamYyzc1ZTIkjHHPyyfFpyfOiQtg3VlBoWkxzSJznS8/edit?usp=sharing)

## Features

- Upload and analyze delivery images
- Uses CLIP model to compare against a list of predefined labels
- Returns the top matched label, confidence score, and a boolean indicating if the image contains valid delivery items
- Supports synchronous processing
- Easily extendable for future scalability

## API Endpoints

### `POST /api/inspect/validate/image/v1/`

**Request:**
```json
{
  "order_id": "123456",
  "image": <image file>
}

