import cv2
import numpy as np
import onnxruntime as ort
from app.config import MODEL_PATH, MODEL_W, MODEL_H, CONFIDENCE, NMS_THRESHOLD, LABEL_PATH


class ONNXPlateModel:
    def __init__(self):
        self.path = MODEL_PATH
        self.MODEL_W = MODEL_W
        self.MODEL_H = MODEL_H
        self.det_conf = CONFIDENCE
        self.nms = NMS_THRESHOLD
        self.labels = self.load_labels()

        self.session = ort.InferenceSession(self.path)
        self.input_name = self.session.get_inputs()[0].name
        self.output_names = [o.name for o in self.session.get_outputs()]

    # -------------------------------
    # Load Labels
    # -------------------------------

    def load_labels(self):
        labels = []
        with open(LABEL_PATH, "r") as f:
            for line in f:
                labels.append(line.strip())
        return labels

    # -------------------------------
    # Preprocess Image
    # -------------------------------

    def preprocess(self, image):
        img = cv2.resize(image, (self.MODEL_W, self.MODEL_H))
        img = img.transpose((2, 0, 1))[::-1]
        img = np.ascontiguousarray(img)
        img = img.astype(np.float32) / 255.0
        img = np.expand_dims(img, axis=0)
        return img

    # -------------------------------
    # Run ONNX Inference
    # -------------------------------

    def infer(self, image):
        return self.session.run(self.output_names, {self.input_name: image})[0]

    # -------------------------------
    # Main Prediction Function
    # -------------------------------

    def predict_plate(self, image_path):
        image = cv2.imread(image_path)

        if image is None:
            return ""

        image = self.resize_pad_image(image)

        img_pre = self.preprocess(image)

        outputs = self.infer(img_pre)

        filtered_boxes, class_ids = self.postprocess(outputs)

        if len(filtered_boxes) == 0:
            return ""

        boxes = [b[:4] for b in filtered_boxes]

        sequence, _ = self.get_character_sequence(boxes, class_ids)

        return sequence

    # -------------------------------
    # Resize + Pad
    # -------------------------------

    @staticmethod
    def resize_pad_image(lp_image):

        width_ = lp_image.shape[1]
        height_ = lp_image.shape[0]

        max_stretch = 416

        if width_ > height_:
            new_width = max_stretch
            new_height = int((height_ * new_width) / width_)
        else:
            new_height = max_stretch
            new_width = int((width_ * new_height) / height_)

        top_padding = int((416 - new_height) / 2)
        side_padding = int((416 - new_width) / 2)

        image_ = cv2.resize(lp_image, (new_width, new_height), interpolation=cv2.INTER_CUBIC)

        reshaped_images = cv2.copyMakeBorder(
            image_,
            top_padding,
            top_padding,
            side_padding,
            side_padding,
            cv2.BORDER_CONSTANT
        )

        return reshaped_images

    # -------------------------------
    # Postprocess Model Output
    # -------------------------------

    def postprocess(self, outputs):

        rows = outputs.shape[1]
        dimensions = outputs.shape[2]

        if dimensions > rows:
            rows = outputs.shape[2]
            dimensions = outputs.shape[1]
            outputs = np.transpose(outputs, (0, 2, 1))

        data = outputs[0]

        classes_scores = data[:, 4:]
        class_ids_all = np.argmax(classes_scores, axis=1)
        max_class_scores = np.max(classes_scores, axis=1)

        valid_indices = np.where(max_class_scores > self.det_conf)[0]

        valid_data = data[valid_indices]
        valid_class_ids = class_ids_all[valid_indices]
        valid_scores = max_class_scores[valid_indices]

        x = valid_data[:, 0]
        y = valid_data[:, 1]
        w = valid_data[:, 2]
        h = valid_data[:, 3]

        left = (x - 0.5 * w).astype(int)
        top = (y - 0.5 * h).astype(int)
        width = w.astype(int)
        height = h.astype(int)

        boxes = [[int(l), int(t), int(w), int(h)] for l, t, w, h in zip(left, top, width, height)]
        confidences = valid_scores.tolist()
        class_ids = valid_class_ids.tolist()

        result = [[int(l), int(t), int(w), int(h), float(conf), int(cid)]
                  for l, t, w, h, conf, cid in zip(left, top, width, height, valid_scores, valid_class_ids)]

        if boxes:

            indices = cv2.dnn.NMSBoxes(boxes, confidences, self.det_conf, self.nms)

            if len(indices) > 0:

                indices = np.array(indices).flatten().tolist()

                class_ids = [class_ids[i] for i in indices]

                result = [result[i] for i in indices]

            else:

                class_ids = []
                result = []

        return result, class_ids

    # -------------------------------
    # Character Sequence (FIXED)
    # -------------------------------

    def get_character_sequence(self, boxes, class_ids):

        if len(boxes) == 0:
            return "", False

        # sort characters left → right
        sorted_indices = np.argsort([b[0] for b in boxes])

        sequence = ""

        for i in sorted_indices:

            cid = class_ids[i]

            if 0 <= cid < len(self.labels):

                sequence += self.labels[cid]

            else:

                sequence += "?"

        return sequence, False