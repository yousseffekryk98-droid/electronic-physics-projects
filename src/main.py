#!/usr/bin/env python3
import time
try:
    import cv2
except ImportError:
    cv2 = None


def main():
    if cv2 is None:
        print("Install dependencies from requirements.txt")
        return
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise SystemExit("Camera not available")
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        # Replace this baseline with the branch README's project-specific detector.
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.putText(frame, f"mean={gray.mean():.1f}", (20, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.imshow("Electronic Physics Project", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
