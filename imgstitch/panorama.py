# 导入必要库
import numpy as np
from imutils import is_cv3, is_cv4
import cv2

class Stitcher:
	def __init__(self):
		# 是否使用cv3或更高版本
		self.isv3 = is_cv3(True)
		# 是否使用cv4或更高版本
		self.isv4 = is_cv4(True)

	def stitch(self, images, ratio=0.75, reprojThresh=4.0, showMatches=False):
		# 用SIFT分别解析两幅图的关键点(kps)与特征(features)
		(imageB, imageA) = images
		(kpsA, featuresA) = self.detectAndDescribe(imageA)
		(kpsB, featuresB) = self.detectAndDescribe(imageB)

		# 找出两幅图的对应关键点与特征
		M = self.matchKeypoints(kpsA, kpsB, featuresA, featuresB, ratio, reprojThresh)

		# 匹配为None则失败
		if M is None: return None

		# 否则进行透视变换拼接图片
		(matches, H, status) = M
		result = cv2.warpPerspective(imageA, H, (imageA.shape[1] + imageB.shape[1], imageA.shape[0]))
		result[0:imageB.shape[0], 0:imageB.shape[1]] = imageB

		# 检查关键点是否实现匹配
		if showMatches:
			vis = self.drawMatches(imageA, imageB, kpsA, kpsB, matches, status)

			# 返回处理后的图片与匹配示意图
			return (result, vis)
		else: return result		# 仅返回处理后的图片

	def detectAndDescribe(self, image):
		# 转换为灰度图
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

		# 因为不同版本调用函数不同，因此需要根据cv版本进行不同的处理
		if self.isv4:
			# 从图片检测并导出特征
			(kps, features) = cv2.SIFT_create().detectAndCompute(image, None)
		elif self.isv3:
			# 从图片检测并导出特征
			descriptor = cv2.xfeatures2d.SIFT_create()
			(kps, features) = descriptor.detectAndCompute(image, None)
		else:
			# 检测图片关键点
			detector = cv2.FeatureDetector_create("SIFT")
			kps = detector.detect(gray)
			# 导出图片特征
			extractor = cv2.DescriptorExtractor_create("SIFT")
			(kps, features) = extractor.compute(gray, kps)

		# 转换关键点为np数组
		kps = np.float32([kp.pt for kp in kps])

		# 返回关键点与特征元组
		return (kps, features)

	def matchKeypoints(self, kpsA, kpsB, featuresA, featuresB, ratio, reprojThresh):
		# 用KNN计算一个粗匹配
		matcher = cv2.DescriptorMatcher_create("BruteForce")
		rawMatches = matcher.knnMatch(featuresA, featuresB, 2)
		matches = []

		# 遍历粗匹配的每个匹配
		for m in rawMatches:
			# 确保两距离之比在ratio内
			if len(m) == 2 and m[0].distance < m[1].distance * ratio:
				matches.append((m[0].trainIdx, m[0].queryIdx))

		# Homograph单应性变换矩阵的计算需要至少4个匹配
		if len(matches) > 4:
			# 把点分为两组
			ptsA = np.float32([kpsA[i] for (_, i) in matches])
			ptsB = np.float32([kpsB[i] for (i, _) in matches])

			# 计算两点集的Homograph单应性变换矩阵
			(H, status) = cv2.findHomography(ptsA, ptsB, cv2.RANSAC, reprojThresh)

			# 返回匹配点、Homograph单应性变换矩阵与每个匹配点的状态
			return (matches, H, status)
		# 否则匹配失败
		else: return None

	def drawMatches(self, imageA, imageB, kpsA, kpsB, matches, status):
		# 初始化
		(hA, wA) = imageA.shape[:2]
		(hB, wB) = imageB.shape[:2]
		vis = np.zeros((max(hA, hB), wA + wB, 3), dtype="uint8")
		vis[0:hA, 0:wA] = imageA
		vis[0:hB, wA:] = imageB

		# 画出每条匹配线
		for ((trainIdx, queryIdx), s) in zip(matches, status):
			# 仅绘制成功匹配的点
			if s == 1:
				ptA = (int(kpsA[queryIdx][0]), int(kpsA[queryIdx][1]))
				ptB = (int(kpsB[trainIdx][0]) + wA, int(kpsB[trainIdx][1]))
				cv2.line(vis, ptA, ptB, (0, 255, 0), 1)
		return vis
