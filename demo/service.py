import os
import platform
import ctypes

class Face(ctypes.Structure):
    _fields_ = [
        ("left", ctypes.c_int),
        ("top", ctypes.c_int),
        ("right", ctypes.c_int),
        ("bottom", ctypes.c_int)
    ]


class RecognizeResult(ctypes.Structure):
    _fields_ = [
        ("person_id", ctypes.c_char * 24),
        ("face_id", ctypes.c_char * 24),
        ("score", ctypes.c_float)
    ]

_path = os.path.join(".", "frsdk", "lib", "linux64", "C", "libFRSDK.so")

_mode = ctypes.cdll.LoadLibrary(_path)

_fd_create_instance = _mode.FD_CreateIns
_fd_create_instance.argtypes = (ctypes.POINTER(ctypes.c_long), )
_fd_create_instance.restype = ctypes.c_int


def fd_create_instance():
    """创建人脸检测实例

    :Parameters:

    :Returns:
      - ``int``，人脸检测实例，如果失败则抛出``Exception``异常
    """
    instance = ctypes.c_long()
    res = _fd_create_instance(instance)
    if res != 0:
        raise Exception("create detect instance failed: {}".format(res))
    return instance.value

_fd_destroy_instance = _mode.FD_DestroyIns
_fd_destroy_instance.argtypes = (ctypes.POINTER(ctypes.c_long), )
_fd_destroy_instance.restype = ctypes.c_int


def fd_destroy_instance(instance):
    """销毁人脸检测实例

    :Parameters:
      - `instance`: ``int``，人脸检测实例

    :Returns:
      - ``int``，0表示销毁成功，如果失败则抛出``Exception``异常
    """
    res = _fd_destroy_instance(ctypes.c_long(instance))
    if res != 0:
        raise Exception("destroy detect instance failed: {}".format(res))
    return 0

_fd_set_params = _mode.FD_SetParams
_fd_set_params.argtypes = (ctypes.c_long, ctypes.c_double, ctypes.c_double)
_fd_set_params.restype = ctypes.c_int


def fd_set_params(instance, min_face_scale=0.05, return_face_scale=1):
    """设置人脸检测参数

    :Parameters:
      - `instance`: ``int``，人脸检测实例
      - `min_face_scale`: ``float``，检测到的人脸大小跟原图比值不能小于该值
      - `return_face_scale`: `int``，返回的人脸区域放大的倍数

    :Returns:
      - ``int``，0表示设置成功，如果失败则抛出``Exception``异常
    """
    res = _fd_set_params(instance, min_face_scale, return_face_scale)
    if res != 0:
        raise Exception("set detect params failed: {} {} {}"
                            .format(res, min_face_scale, return_face_scale))
    return 0

_fd_detect_face = _mode.FD_DetectFace
_fd_detect_face.argtypes = (ctypes.c_long, ctypes.c_char_p, ctypes.c_int)
_fd_detect_face.restype = ctypes.c_int


def fd_detect_face(instance, content):
    """检测人脸

    :Parameters:
      - `instance`: ``int``，人脸检测实例
      - `content`: ``bytes``，要检测的图片文件内容

    :Returns:
      - ``int``，0表示检测成功，如果失败则抛出``Exception``异常
    """
    res = _fd_detect_face(instance, content, len(content))
    if res != 0:
        raise Exception("detect face failed: {}".format(res))
    return 0

_fd_get_face_number = _mode.FD_GetFaceNum
_fd_get_face_number.argtypes = (ctypes.c_long, ctypes.POINTER(ctypes.c_int))
_fd_get_face_number.restype = ctypes.c_int


def fd_get_face_number(instance):
    """获取检测到的人脸数

    :Parameters:
      - `instance`: ``int``，人脸检测实例

    :Returns:
      - ``int``，检测到的人脸数，如果失败则抛出``Exception``异常
    """
    number = ctypes.c_int()
    res = _fd_get_face_number(instance, number)
    if res != 0:
        raise Exception("get face number failed: {}".format(res))
    return number.value

_fd_get_face = _mode.FD_GetFace
_fd_get_face.argtypes = (ctypes.c_long, ctypes.c_int, ctypes.POINTER(Face))
_fd_get_face.restype = ctypes.c_int


def fd_get_face(instance, no):
    """获取检测到的人脸

    :Parameters:
      - `instance`: ``int``，人脸检测实例
      - `no`: ``int``，第几个

    :Returns:
      - ``list``，检测到的人脸，列表的四个元素分别为人脸在原图中的左上角和右下角坐标，
      如果失败则抛出``Exception``异常
    """
    face = Face()
    res = _fd_get_face(instance, no, face)
    if res != 0:
        raise Exception("get face failed: {} {}".format(res, no))
    return [face.left, face.top, face.right, face.bottom]

_fr_create_new_gallery = _mode.FR_CreateNewGallery
_fr_create_new_gallery.argtypes = (ctypes.c_char_p, )
_fr_create_new_gallery.restype = ctypes.c_int


def fr_create_new_gallery(gallery_path):
    """创建人脸库

    :Parameters:
      - `gallery_path`: ``str``，人脸库文件路径

    :Returns:
      - ``int``，0表示创建成功，如果失败则抛出``Exception``异常
    """
    res = _fr_create_new_gallery(gallery_path.encode())
    if res != 0:
        raise Exception("create gallery failed: {} {}"
                            .format(res, gallery_path))
    return 0

_fr_create_instance = _mode.FR_CreateIns
_fr_create_instance.argtypes = (ctypes.POINTER(ctypes.c_long), ctypes.c_char_p)
_fr_create_instance.restype = ctypes.c_int


def fr_create_instance(model_path):
    """创建人脸识别实例

    :Parameters:
      - `model_path`: ``str``，模型文件路径

    :Returns:
      - ``int``，0表示创建成功，如果失败则抛出``Exception``异常
    """
    instance = ctypes.c_long()
    res = _fr_create_instance(instance, model_path.encode())
    if res != 0:
        raise Exception("create recognize instance failed: {} {}"
                            .format(res, model_path))
    return instance.value

_fr_destroy_instance = _mode.FR_DestroyIns
_fr_destroy_instance.argtypes = (ctypes.POINTER(ctypes.c_long), )
_fr_destroy_instance.restype = ctypes.c_int


def fr_destroy_instance(instance):
    """销毁人脸识别实例

    :Parameters:
      - `instance`: ``int``，人脸识别实例

    :Returns:
      - ``int``，0表示销毁成功，如果失败则抛出``Exception``异常
    """
    res = _fr_destroy_instance(ctypes.c_long(instance))
    if res != 0:
        raise Exception("destroy recognize instance failed: {}"
                            .format(res))
    return 0

_fr_load_faces = _mode.FR_LoadFaces
_fr_load_faces.argtypes = (ctypes.c_long, ctypes.c_char_p)
_fr_load_faces.restype = ctypes.c_int

_fr_set_params = _mode.FR_SetParams
_fr_set_params.argtypes = (ctypes.c_long, ctypes.c_int, ctypes.c_double)
_fr_set_params.restype = ctypes.c_int


def fr_set_params(instance, face_choose_type=1, min_face_scale=0.05):
    """设置人脸识别参数

    :Parameters:
      - `instance`: ``int``，人脸识别实例
      - `face_choose_type`: ``int``，在图片中检测到多张人脸时，0表示不自动选择最大的人脸，
      1表示自动选择最大的人脸

    :Returns:
      - ``int``，0表示设置成功，如果失败则抛出``Exception``异常
    """
    res = _fr_set_params(instance, face_choose_type, min_face_scale)
    if res != 0:
        raise Exception("set recognize params failed: {} {} {}"
                            .format(res, face_choose_type, min_face_scale))
    return 0


def fr_load_faces(instance, gallery_path):
    """加载人脸库

    :Parameters:
      - `instance`: ``int``，人脸识别实例
      - `gallery_path`: ``str``，人脸库文件路径

    :Returns:
      - ``int``，0表示加载成功，如果失败则抛出``Exception``异常
    """
    res = _fr_load_faces(instance, gallery_path.encode())
    if res != 0:
        raise Exception("load faces failed: {} {}"
                            .format(res, gallery_path))
    return 0

_fr_save_faces = _mode.FR_SaveFaces
_fr_save_faces.argtypes = (ctypes.c_long, ctypes.c_char_p, ctypes.c_bool)
_fr_save_faces.restype = ctypes.c_int


def fr_save_faces(instance, gallery_path, save_all=False):
    """保存内存中的人脸库到磁盘

    :Parameters:
      - `instance`: ``int``，人脸识别实例
      - `gallery_path`: ``str``，人脸库文件路径
      - `save_all`: ``bool``，是否全量写入，默认增量

    :Returns:
      - ``int``，0表示保存成功，如果失败则抛出``Exception``异常
    """
    res = _fr_save_faces(instance, gallery_path.encode(), save_all)
    if res != 0:
        raise Exception("save faces failed: {} {}"
                            .format(res, gallery_path))
    return 0

_fr_add_face = _mode.FR_AddFace
_fr_add_face.argtypes = (ctypes.c_long, ctypes.c_char_p, ctypes.c_int,
                         ctypes.c_char * 24, ctypes.c_char * 24,
                         ctypes.POINTER(ctypes.c_int))
_fr_add_face.restype = ctypes.c_int


def fr_add_face(instance, content, person_id, face_id):
    """添加人脸到库中

    :Parameters:
      - `instance`: ``int``，人脸识别实例
      - `content`: ``bytes``，人脸图片文件内容
      - `person_id`: `str``，人脸所属人的ID
      - `face_id`: ``str``，人脸ID

    :Returns:
      - ``int``，结果码，0表示添加成功，1表示从人脸图片中检测到的人脸数不对，
      2表示（person_id+face_id）重复，如果失败则抛出``Exception``异常
      结果码为1时，如果face_choose_type参数为0表示人脸数不为1，为1时则表示人脸数为0
    """
    status = ctypes.c_int()
    res = _fr_add_face(instance, content, len(content),
                       (ctypes.c_char * 24)(*person_id.encode()),
                       (ctypes.c_char * 24)(*face_id.encode()),
                       status)
    if res != 0:
        raise Exception("add face failed: {} {} {}"
                            .format(res, person_id, face_id))

    return status.value

_fr_del_face = _mode.FR_DelFace
_fr_del_face.argtypes = (ctypes.c_long, ctypes.c_char * 24, ctypes.c_char * 24,
                         ctypes.POINTER(ctypes.c_int))
_fr_del_face.restype = ctypes.c_int


def fr_del_face(instance, person_id, face_id):
    """删除人脸

    :Parameters:
      - `instance`: ``int``，人脸识别实例
      - `person_id`: `str``，人脸所属人的ID
      - `face_id`: ``str``，人脸ID

    :Returns:
      - ``int``，结果码，0表示删除成功，1表示该人脸不存在
    """
    status = ctypes.c_int()
    res = _fr_del_face(instance, (ctypes.c_char * 24)(*person_id.encode()),
                       (ctypes.c_char * 24)(*face_id.encode()), status)
    if res != 0:
        raise Exception("del face failed: {} {} {}"
                            .format(res, person_id, face_id))

    return status.value

_fr_recognize = _mode.FR_Recognize
_fr_recognize.argtypes = (ctypes.c_long, ctypes.c_char_p, ctypes.c_int,
                          ctypes.POINTER(ctypes.c_int),
                          ctypes.POINTER(RecognizeResult),
                          ctypes.POINTER(ctypes.c_bool), ctypes.c_int)
_fr_recognize.restype = ctypes.c_int


def fr_recognize(instance, content, max_number=10, min_score=None, strategy=2):
    """识别图片中的人

    :Parameters:
      - `instance`: ``int``，人脸识别实例
      - `content`: ``bytes``，要识别的图片文件内容
      - `max_number`: `int``，最多返回的人数
      - `min_score`: ``float``，最低置信度要求
      - `strategy`: ``int``，识别策略
        0: 在FaceID级排序，返回结果中，同一个PersonID可能有多张人脸命中
        1: 在PersonID级排序，返回结果中，同一个PersonID只可能有一张人脸命中，
        用同一PersonID下所有人脸中最大得分作为此PersonID得分
        2: 在PersonID级排序，返回结果中，同一个PersonID只可能有一张人脸命中，
        用同一PersonID下所有人脸的平均得分作为此PersonID得分

    :Returns:
      - (``bool``, ``list``)，第一个元素表示是否识别成功，第二个元素为可能的人，
      如果失败则抛出``Exception``异常
    """
    number = ctypes.c_int(max_number)
    persons = (RecognizeResult * max_number)()
    status = ctypes.c_bool()
    res = _fr_recognize(instance, content, len(content), number,
                        ctypes.pointer(persons[0]), status, strategy)
    if res != 0:
        raise Exception("recognize face failed: {} {} {}"
                            .format(res, max_number, min_score))

    if not status.value:
        return False, []

    number = number.value
    persons = [{
        'person_id': v.person_id.decode(),
        'face_id': v.face_id.decode(),
        'score': v.score
    } for v in persons[:number]]

    if min_score is not None:
        persons = [v for v in persons if v['score'] >= min_score]

    return True, persons
