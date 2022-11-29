import cv2
import numpy as np
import time

ARUCO_DICT = cv2.aruco.DICT_4X4_50

MIN_ECC = 0.014
MAX_ECC = 0.020

class InputDetection:
    def __init__(self):
        self.aruco_dict  = cv2.aruco.Dictionary_get(ARUCO_DICT)
        self.aruco_param = cv2.aruco.DetectorParameters_create()

        self.video_feed  = cv2.VideoCapture(0)

        self.img_markers = {}

    def detection_loop(self, show=False):
        # Capture video frame
        _, frame = self.video_feed.read()
        self._find_markers(frame, show)

        # Check for GO marker
        if 0 in self.img_markers:
            omega = self._calculate_precession()
            ecc   = self._calculate_eccentricity()

            return (omega, ecc)

        return (None, None)


    def _find_markers(self, img, show=False):
        # Initialize marker array
        self.img_markers = {}

        corners, ids, rejected = cv2.aruco.detectMarkers(img, self.aruco_dict, parameters=self.aruco_param)
        # if (corners is None or ids is None):
        #     print ('[ERROR] No markers found')
        #     cv2.imshow('ERROR', img)
        #     cv2.waitKey(5000)
        #     return

        # Show image and markers
        if show:
            print('[INFO] Showing markers')
            img_copy = img.copy()
            cv2.aruco.drawDetectedMarkers(img_copy, corners, ids)

            cv2.imshow('Markers', img_copy)
            cv2.waitKey(5000)

        # Save marker info in the format
        # {#id : [[.., ..], [.., ..], .., ..], #id: []}
        for id, marker in zip(ids, corners):
            if (id < 25):
                self.img_markers[id[0]] = marker.astype('int32')[0]

    def _calculate_precession(self):
        earth_marker = self.img_markers[1]

        del_x = earth_marker[1][0] - earth_marker[0][0]
        del_y = earth_marker[1][1] - earth_marker[0][1]

        return np.degrees(np.arctan2(del_y, del_x))

    def _calculate_eccentricity(self):
        earth_marker = self._marker_center(self.img_markers[1])
        sun_marker   = self._marker_center(self.img_markers[2])

        dist = self._distance(earth_marker, sun_marker)

        # Markers used to determine radius of orbit
        inner_marker = self._distance(self._marker_center(self.img_markers[3]), sun_marker)
        outer_marker = self._distance(self._marker_center(self.img_markers[4]), sun_marker)

        if (dist < outer_marker) and (dist > inner_marker):
            # Earth in circular orbit 
            return MIN_ECC

        else: 
            return MAX_ECC

    def _distance(self, point1, point2):
        return np.sqrt(np.sum(np.square(np.array(point1) - np.array(point2))))

    def _marker_center(self, marker):
        x_ = (marker[0][0] + marker[2][0]) / 2
        y_ = (marker[0][1] + marker[2][1]) / 2

        return (x_, y_)


def test():
    inp = InputDetection()

    while True:
        omega, ecc = inp.detection_loop(True)

        if not omega is None: 
            print(f'Precession angle: {omega}')

        time.sleep(0.5)


