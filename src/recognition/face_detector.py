from ultralytics import YOLO
import numpy as np
import cv2
from config.config import Config
from src.utils.logger import setup_logger

logger = setup_logger()

class FaceDetector:
    def __init__(self):
        """Initialize the YOLOv8 face detector"""
        try:
            self.model = YOLO(Config.MODEL_PATH)
            self.conf_threshold = Config.FACE_DETECTION_CONFIDENCE
            logger.info("Face detector initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing face detector: {e}")
            raise

    def detect_faces(self, frame):
        """
        Detect faces in the given frame using YOLOv8
        
        Args:
            frame: Input image frame (numpy array)
            
        Returns:
            List of face locations in (top, right, bottom, left) format
        """
        try:
            # Run YOLOv8 inference
            results = self.model(frame, conf=self.conf_threshold)
            
            # Convert YOLOv8 boxes to face_recognition format
            face_locations = []
            
            if len(results) > 0:
                boxes = results[0].boxes
                for box in boxes:
                    # Get coordinates
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    
                    # Convert to integers
                    top = int(y1)
                    right = int(x2)
                    bottom = int(y2)
                    left = int(x1)
                    
                    face_locations.append((top, right, bottom, left))
                    
                logger.debug(f"Detected {len(face_locations)} faces")
            
            return face_locations

        except Exception as e:
            logger.error(f"Error in face detection: {e}")
            return []

    def draw_faces(self, frame, face_locations):
        """
        Draw rectangles around detected faces
        
        Args:
            frame: Input image frame
            face_locations: List of face locations
            
        Returns:
            Frame with drawn rectangles
        """
        try:
            for face_location in face_locations:
                top, right, bottom, left = face_location
                
                # Draw rectangle
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                
                # Draw confidence score if available
                if hasattr(face_location, 'conf'):
                    conf = face_location.conf
                    cv2.putText(frame, 
                              f"Conf: {conf:.2f}", 
                              (left, top - 10),
                              cv2.FONT_HERSHEY_SIMPLEX,
                              0.5,
                              (0, 255, 0),
                              2)
            
            return frame

        except Exception as e:
            logger.error(f"Error drawing faces: {e}")
            return frame

    def preprocess_frame(self, frame):
        """
        Preprocess frame before detection
        
        Args:
            frame: Input image frame
            
        Returns:
            Preprocessed frame
        """
        try:
            # Resize if needed
            if frame.shape[1] > Config.FRAME_WIDTH:
                scale = Config.FRAME_WIDTH / frame.shape[1]
                frame = cv2.resize(frame, None, fx=scale, fy=scale)
            
            # Convert to RGB if needed
            if len(frame.shape) == 2:
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
            
            return frame

        except Exception as e:
            logger.error(f"Error preprocessing frame: {e}")
            return frame

    def get_face_embeddings(self, frame, face_locations):
        """
        Get face embeddings for detected faces
        
        Args:
            frame: Input image frame
            face_locations: List of face locations
            
        Returns:
            List of face embeddings
        """
        try:
            embeddings = []
            for face_location in face_locations:
                top, right, bottom, left = face_location
                
                # Extract face ROI
                face_image = frame[top:bottom, left:right]
                
                # Get embedding (implement your embedding method here)
                # This is a placeholder
                embedding = np.zeros(128)
                
                embeddings.append(embedding)
            
            return embeddings

        except Exception as e:
            logger.error(f"Error getting face embeddings: {e}")
            return []
