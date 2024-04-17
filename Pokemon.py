class Pokemon:
    def __init__(self, _id):
        self._id = _id
        self._name = None
        self._silhouetteImageURI = None
        self._originalImageURI = None
        self._isAnswer = False

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_silhouette_image_uri(self):
        return self._silhouetteImageURI

    def get_original_image_uri(self):
        return self._originalImageURI

    def get_is_answer(self):
        return self._isAnswer

    def set_name(self, name):
        self._name = name

    def set_silhouette_image_uri(self, silhouette_image_uri):
        self._silhouetteImageURI = silhouette_image_uri

    def set_original_image_uri(self, original_image_uri):
        self._originalImageURI = original_image_uri

    def set_is_answer(self, is_answer):
        self._isAnswer = is_answer

    def to_dict(self):
        return {
            "_id": self._id,
            "_name": self._name,
            "_silhouetteImageURI": self._silhouetteImageURI,
            "_originalImageURI": self._originalImageURI,
            "_isAnswer": self._isAnswer
        }
