/*
 * 人脸识别FRSDK动态链接库头文件
 *
 * @author		邓亚峰<dengyafeng@gmail.com>, 叶伟龙 <weilong.ye.2012@gmail.com>
 * @version		1.0
 * @since		2014-4-24
 */

#ifndef FRSDK_H_
#define FRSDK_H_

#ifdef FRSDK_EXPORTS
	#define FRSDK_API __declspec(dllexport)
#else
	#define FRSDK_API __declspec(dllimport)	
#endif

#ifdef __cplusplus
extern "C" {
#endif

//---------------------------------------------------------------------------------------------------------------------------------

/*
 * 错误返回码
 */
#define FRSDKE_OK                                    0
#define FRSDKE_INVALID_INSTANCE                      -10001
#define FRSDKE_INVALID_FACE_ID                       -10000 
#define FRSDKE_BAD_ALLOC                             -9999
#define FRSDKE_FACE_DETECT_INIT_MODEL_FAILED         -9998
#define FRSDKE_FACE_RECOGNIZE_INIT_MODEL_FAILED      -9997
#define FRSDKE_INVALID_INPUT_ARGUMENTS               -9996
#define FRSDKE_INVALID_OUTPUT_ARGUMENTS              -9995
#define FRSDKE_OPEN_FACES_FILE_FAIL                  -9994
#define FRSDKE_READ_FACES_FILE_FAIL                  -9993
#define FRSDKE_WRITE_FACES_FILE_FAIL                 -9992
#define FRSDKE_WRONG_FACES_FILE                      -9991

//---------------------------------------------------------------------------------------------------------------------------------

/*
 * 人脸检测结果
 */
struct Rect
{
	int left;		// 人脸检测框左上角x坐标
	int top;		// 人脸检测框左上角y坐标
	int right;		// 人脸检测框右下角x坐标
	int bottom;		// 人脸检测框右下角y坐标
};

/*
 * 人脸识别返回结果
 */
struct FaceRecogRlt
{
	char personID[24];	// 人ID
	char faceID[24];	// 人脸ID，某个人可能在人脸库存有多张脸，通过此ID区分
	float fScore;		// 与人脸（nPersonID,nFaceID）的匹配置信度
};

//---------------------------------------------------------------------------------------------------------------------------------

/*
 * 接口函数列表
 *
 * 人脸检测接口，FD_*
 *
 * FRSDK_API int FD_CreateIns(long* pIns);	
 * FRSDK_API int FD_DestroyIns(long* pIns);
 * FRSDK_API int FD_SetParams(long ins, double dMinDetWidthRatio, double dFaceRectExpandRatio);
 * FRSDK_API int FD_DetectFace(long ins, const char* pImgBuf, int nBufSize);
 * FRSDK_API int FD_GetFaceNum(long ins, int* pnFaceNum);
 * FRSDK_API int FD_GetFace(long ins, int id, DetFace* pDetFace);
 *
 * 人脸建模和识别接口，FR_* 
 *
 * FRSDK_API int FR_CreateIns(long* pIns, const char* strModelDir);
 * FRSDK_API int FR_DestroyIns(long* pIns);
 * FRSDK_API int FR_CreateNewGallery(const char* strGalleryFilename);
 * FRSDK_API int FR_LoadFaces(long ins, const char* strGalleryFilename);
 * FRSDK_API int FR_SaveFaces(long ins, const char* strGalleryFilename);
 * FRSDK_API int FR_AddFace(long ins, const char* pImgBuf, int nBufSize, const char personID[24], const char faceID[24], int* pnStatus);
 * FRSDK_API int FR_Recognize(long ins, const char* pImgBuf, int nBufSize, int* pnRetRltNum, FaceRecogRlt* pRltArr, bool* pIsOneFace);
 */

//---------------------------------------------------------------------------------------------------------------------------------

/*
 * 创建人脸检测实例
 *
 * 必须先于任何其它人脸检测接口调用 
 *
 * @param pIns, 输出参数，存放一个内部检测类实例指针
 * @return FRSDKE_OK, 成功创建
 */
FRSDK_API int FD_CreateIns(long* pIns);	

/*
 * 销毁人脸检测实例
 *
 * 必须与FD_CreateIns(pIns)成对调用
 *
 * @param pIns, 输入参数，需要销毁的人脸检测实例，销毁后(*pIns)将被设为0
 * @return FRSDKE_OK, 成功销毁
 */
FRSDK_API int FD_DestroyIns(long* pIns);

/*
 * 设置人脸检测参数
 * 若不调用此接口，默认值为dMinDetWidthRatio=0.05
 *
 * @param ins, 输入参数，人脸检测实例
 * @param dMinDetWidthRatio, 输入参数，设定能检测到的最小人脸框尺寸，例如输入图像 width=1000，hight=1500，设置dMinDetWidthRatio=0.1，则最小检测框尺寸为150=1500*0.1
 * @param dRaceRectExpandRatio, 输入参数，设定结果检测框扩展倍率，需>=1.0
 * @return FRSDKE_OK, 成功设置
 */
FRSDK_API int FD_SetParams(long ins, double dMinDetWidthRatio, double dFaceRectExpandRatio);

/*
 * 检测人脸
 *
 * 结果的返回另有接口，此接口只进行人脸检测动作
 *
 * @param ins, 输入参数，人脸检测实例
 * @param pImgBuf, 输入参数，待检测的输入图像数据首地址，可为BMP,JPG,PNG格式的原始数据
 * @param nBufSize, 输入参数，内存图像数据字节数
 * @return FRSDKE_OK, 成功检测
 */
FRSDK_API int FD_DetectFace(long ins, const char* pImgBuf, int nBufSize);

/*
 * 获取检测到的人脸数目
 * 
 * @param ins, 输入参数，人脸检测实例
 * @param pnFaceNum, 输出参数，存放人脸数目
 * @return FRSDKE_OK, 成功获取
 */
FRSDK_API int FD_GetFaceNum(long ins, int* pnFaceNum);

/*
 * 获取检测到的某一个人脸
 *
 * @param ins, 输入参数，人脸检测实例
 * @param id, 输入参数，取出第id个检测到的人脸，取值范围为[0,nFaceNum-1], nFaceNum为FD_GetFaceNum()的输出结果
 * @param pDetFace, 输出参数，存放获取到的单个人脸
 * @return FRSDKE_OK, 成功获取
 */
FRSDK_API int FD_GetFace(long ins, int id, Rect* pRect);

//---------------------------------------------------------------------------------------------------------------------------------

/*
 * 创建一个新的、空的人脸库
 * 在内部为静态函数，不需创建实例即可调用
 *
 * @param strGalleryFilename, 输入参数，人脸库路径
 * @return FRSDKE_OK, 成功创建
 */
FRSDK_API int FR_CreateNewGallery(const char* strGalleryFilename);

/*
 * 创建人脸识别实例（包含建模和识别功能）
 * 
 * 创建多个实例的时候，模型文件只会在创建第一个实例的时候被装载，后面的实例不会重复装载模型
 * 这里的模型文件是算法需要用到的模型文件，不是人脸建模后所存储的人脸模型库
 * 
 * @param pIns, 输出参数，存放一个内部人脸识别类实例指针
 * @param strModelDir, 输入参数，人脸识别模型文件夹，存放了人脸识别模块所需要用到的所有模型文件，里面的文件结构和文件名称均不能变动
 * @return FRSDKE_OK, 成功创建
 */
FRSDK_API int FR_CreateIns(long* pIns, const char* strModelDir);

/*
 * 销毁人脸检测实例
 *
 * 必须与FR_CreateIns(pIns)成对调用
 *
 * @param pIns, 输入参数，需要销毁的人脸识别实例，销毁后(*pIns)将被设为0
 * @return FRSDKE_OK, 成功销毁
 */
FRSDK_API int FR_DestroyIns(long* pIns);

/*
 * 装载人脸库
 *
 * 人脸库里的每一个人脸模型包含有外部输入的ID信息和内部提取的特征信息，并不包含图像原始数据
 *
 * @param ins, 输入参数，人脸识别实例
 * @param strGalleryFilename, 需要装载的人脸库路径
 * @return FRSDKE_OK, 成功装载
 */
FRSDK_API int FR_LoadFaces(long ins, const char* strGalleryFilename);

/* 
 * 存储人脸库
 * 增量存储方式，假如strGalleryFilename存在，通过FR_AddFace()添加的人脸将被追加到文件末尾
 *
 * @param ins, 输入参数，人脸识别实例
 * @param strGalleryFilename, 人脸库存储路径
 * @return FRSDKE_OK, 成功保存
 */
FRSDK_API int FR_SaveFaces(long ins, const char* strGalleryFilename);

/*
 * 人脸建模
 *
 * 输入一张人脸图像数据和ID信息，特征数据被提取后连同ID信息被加入到内存的人脸库中
 * 如需存入硬盘，需后续调用FR_SaveFaces()。可以在多次调用FR_AddFace()加入多张人脸后，再FR_SaveFaces()
 *
 * @param ins, 输入参数，人脸识别实例
 * @param pImgBuf, 输入参数，待检测的输入图像数据首地址，可为BMP,JPG,PNG格式的原始数据
 *	输入图像只能包含一张人脸，可以在人脸检测框的基础上适当扩大人脸框，裁切后作为此输入。内部人脸检测设置的最小检测框参数为0.2
 * @param nBufSize, 输入参数，内存图像数据字节数
 * @param personID, 输入参数，人脸所属的人ID
 * @param faceID, 输入参数，人脸ID
 * @param pnStatus, 状态返回信息，不同于函数的返回码，函数的返回码用来返回错误信息
 *	0：正常加入人脸； 1：此输入图像检测到的人脸数目不为1； 2：人脸库里已有与输入相同的ID信息(相同的PersonID和FaceID)
 * @return FRSDKE_OK, 成功加入
 */
FRSDK_API int FR_AddFace(long ins, const char* pImgBuf, int nBufSize, const char personID[24], const char faceID[24], int* pnStatus);

/*
 * 人脸识别
 * 
 * @param ins, 输入参数，人脸识别实例
 * @param pImgBuf, 输入参数，待检测的输入图像数据首地址，可为BMP,JPG,PNG格式的原始数据
 *	输入图像只能包含一张人脸，可以在人脸检测框的基础上适当扩大人脸框，裁切后作为此输入。内部人脸检测设置的最小检测框参数为0.2
 * @param nBufSize, 输入参数，内存图像数据字节数
 * @param pnRetRltNum, 输入输出参数，设置识别结果的返回数目
 *  若人脸库人数PersonNum<(*pnRetRltNum)，则只有PersonNum个有效结果被返回，且(*pnRetRltNum)将被作为输出参数返回有效的结果数目
 * @param pRltArr, 输出参数，识别结果返回数组，需在外部申请空间，申请大小需 >= (*pnRetRltNum)
 * @param pIsOneFace, 输出参数，true: 输入图像只检测到一张人脸，识别结果有效； false: 输入图像检测到的人脸数不为1，识别结果无效
 * @return FRSDKE_OK, 成功识别
 */
FRSDK_API int FR_Recognize(long ins, const char* pImgBuf, int nBufSize, int* pnRetRltNum, FaceRecogRlt* pRltArr, bool* pIsOneFace);

//---------------------------------------------------------------------------------------------------------------------------------

#ifdef __cplusplus
}
#endif

#endif // end of FRSDK_H_
