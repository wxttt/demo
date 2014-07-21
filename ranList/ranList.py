__author__ = 'wangxiaottt'
# -*- coding: utf-8 -*-



class IdList:
    # 生成一个num大小的序列, 并指向firstnum
    def __init__(self, nums, firstnum): pass

    # 添加nums的歌，[0,1,2,3,4]在3后面加入2首歌，则nums=[4,5], nums需要是升序排列
    def addNum(self, nums): pass

    # 删除nums的歌，[0,1,2,3,4]中删掉1，4，则nums=[1,4], nums需要是升序排列
    def removeNum(self, nums): pass

    # 当前所在的num
    def current(self): pass

    # 去到num，直接切歌
    def go(self, num): pass

    # 返回下一个idx, 用于移动端左右切换ui显示
    def getNext(self): pass

    # 移动到下一个idx, 并返回
    def goNext(self): pass

    # 返回上一个idx, 用于移动端左右切换ui显示
    def getPrevious(self): pass

    # 移动到上一个idx, 并返回
    def goPrevious(self): pass

# 顺序列表
class OrderedIdList(IdList):
    def __init__(self, nums, firstnum):
        # 序列数量
        self.nums = nums

        # 目前所在的位置
        self.current = firstnum

    def addNum(self, nums):
        for n in nums:
            # 添加的数字序列在idx之前（包括相等），那么idx+1
            if n <= self.current:
                self.current = self.current + 1
            else:
                break

        self.nums = self.nums + len(nums)

    def removeNum(self, nums):
        self.nums = self.nums - len(nums)

        if self.nums == 0:
            self.current = None
            return None

        for n in nums:
            # 删除的数字序列在idx之后（包括相等），那么idx+1
            if n < self.current:
                self.current = self.current - 1
            else:
                break;

        return self.current

    def current(self):
        return self.current

    def go(self, num):
        self.current = num

    def getNext(self):
        if self.nums == 0:
            return None
        if self.current == None:
            return 0
        return (self.current + 1) % self.num

    def goNext(self):
        self.current = self.getNext()

        return self.current

    def getPrevious(self):
        if self.nums == 0:
            return None
        if self.current == None:
            return self.num - 1
        return (self.current + self.num - 1) % self.num

    def goPrevious(self):
        self.current = self.getPrevious()

        return self.current


import random

# 随机播放列表（下面以12345这5首歌为例，-表示序列后面的数字是前进播放，=表示序列后面的数字是回退操作）
# a. 前进时发现无数据，将生产一个随机序列，生产的随机队列第一个数字不上个序列最后一个数字相同
#        从空列表开始 -24513，播放到3时 -54231， -24
# b. 回退将回溯到之前的播放，将保存上一次的播放序列保证回溯操作的连贯性
#        从之前4回退， =2 =13245
# c. 回退到播放历史不存在的时候仍回退将在最后一个序列中无限循环
#        继续回退，=13245 =13
# d. 回退后的前进操作将先按之前的播放序列继续播放
#    前进-1 -54231 -24……

# thread not safe, invoke in UI thread ！！

class RandomIdList(IdList):
    def __init__(self, nums, firstnum):
        # “随机队列”列表，每项是一个随机播放列表
        self.lists = []
        self.addOneList(nums, firstnum)
        self.idxx = 0
        self.idxy = 0 if nums else None

        # 是否进入多次循环，见getPrevious函数
        self.previousrepeatfirstlist = False

    # 添加序列为nums的歌，12345在4后面加入2首歌，则nums=[5,6], nums需要是升序排列
    def addNum(self, nums):
        # 把队列中大于nums的数字升个级，变成123467
        for idxx in range(0, len(self.lists)):
            list = self.lists[idxx]
            for idxy in range(0, len(list)):
                i = 0
                n = lists[idxy]
                for num in nums:
                    if num <= n:
                        i = i + 1
                    else:
                        break
                if i != 0:
                    list[idxy] = list[idxy] + i

        # 只修改最新的列表，过去的列表不管了
        # 把当前播放位置之后添加进来这几首歌，添加到前面previous会错
        behind = -1
        if self.idxx == len(self.lists) - 1:
            behind = self.idxy

        toshuffle = self.lists[len(self.lists) - 1][behind + 1:] + nums
        toshuffle = random.shuffle(toshuffle)

        self.lists[len(self.lists) - 1] = self.lists[len(self.lists) - 1][:behind + 1] + toshuffle

    # 用于有播放列表概念的地方，web/pc端
    # 删除序列为nums的歌，12345在删除1、3两首歌，则nums=[0,2], nums需要是升序排列
    def removeNum(self, nums):
        idxyDel = False

        for idxx in range(0, len(self.lists)):
            # 如果是self.idxx所在的序列，需要处理下self.idxy
            changey = (idxx == self.idxx)
            # idx的变化
            idxdel = 0
            list = self.lists[idxx]
            # 变化后的list
            newlist = []
            for idxy in range(0, len(list)):
                remove = False
                numdel = 0

                for i in nums:
                    if list[idxy] == i:
                        remove = True
                        if changey：

                        if self.idxy >= i:
                            idxdel++
                        if self.idxy == i:
                            idxyDel = True
                    break
                elif list[idxy] > i:
                numdel = numdel + 1
            else:
                break

        if not remove:
            newlist.append(list[idxy])


        if changey:
            self.idxy = self.idxy - idxdel
            if self.idxy < 0
            self.idxy = None

        self.lists[idxx] = newlist

        if idxyDel:
            return self.goNext()

        return self.current();


def current():
    return self.get(self.idxx, self.idxy)

    def get(idxx, idxy):
        if idxy == None:
            return None
        return self.lists[idxx][idxy]

# 返回下一个随机idx， 用于移动端左右切换ui显示
def getNext(self):
    idxx, idxy, f = self.getNext0()
    return self.get(idxx, idxy)


def getNext0(self):
    # 删空了，别想点了
    if len(self.lists[len(self.lists) - 1]) == 0:
        return self.idxx, None, None

    idxx = self.idxx
    idxy = (self.idxy + 1) if (self.idxy != None) else 0
    finishpreviousrepeatfirstlist = False

    if idxy == len(self.lists[self.idxx]):
        if self.previousrepeatfirstlist:
            idxx = 0
            finishpreviousrepeatfirstlist = True
        else:
            idxx = self.idxx + 1
            if idxx == len(self.lists):
                self.addOneList(len(self.lists[self.idxx - 1]))

    return idxx, idxy, finishpreviousrepeatfirstlist

# 跳到下一个随机idx
def goNext(self):
    self.idxx, self.idxy, finishpreviousrepeatfirstlist = self.getNext()

    # 保证不会多余2个序列
    if len(self.lists) == 3:
        del self.lists[0]
        self.idxx = self.idxx - 1

    if finishpreviousrepeatfirstlist:
        self.previousrepeatfirstlist = False

    return self.current();

    def getPrevious(self):
        idxx, idxy, r = self.getPrevious0()
        return self.get(idxx, idxy)


def getPrevious0(self):
    # 删空了，别想点了
    if len(self.lists[len(self.lists) - 1]) == 0:
        return self.idxx, None, None

    idxx = self.idxx
    idxy = (self.idxy - 1) if (self.idxy != None) else -1
    repeatfirstlist = False

    if idxy == -1:
        idxx = idxx - 1

        if idxx == -1:
            idxx = 0
            # 进入过第一队列的多次循环中
            repeatfirstlist = True

        idxy = len(self.lists[idxx]) - 1

    return idxx, idxy, repeatfirstlist


def goPrevious(self):
    self.idxx, self.idxy, repeatfirstlist = self.getPrevious0()

    if repeatfirstlist:
        self.previousrepeatfirstlist = True

    return self.current()


# 添加一个num长的随机序列
def addOneList(self, nums, firstnum):
    lastnum = -1
    if len(self.lists) != 0:
        lastlist = self.lists[len(self.lists) - 1]
        lastnum = lastlist[len(lastlist) - 1]

    self.lists.append(self.genRandIds(nums, lastnum, firstnum))

# 生成随机id列表，使得第一个数字是firstnum, 不是notfirstnum（当队列长度大于1时）
def genRandIds(self, nums, notfirstnum, firstnum):
    randomids = range(0, num)
    random.shuffle(randomids)

    if randomids[0] != firstnum and nums == 1 and firsnum != None:
        toswitch = randomids.index(firstnum)
    randomids[0], randomids[toswitch] = randomids[toswitch], randomids[0]

    if randomids[0] == notfirstnum and nums != 1 and notfirstnum != None:
        toswitch = random.randint(1, nums - 1)
        randomids[0], randomids[toswitch] = randomids[toswitch], randomids[0]

    return randomids


r = RandomList(10);
print '-',
for i in range(0, 25):
    print r.getNext(),

print ''
print '=',
for i in range(0, 42):
    print r.getPrevious(),

print ''
print '-',
for i in range(0, 55):
    print r.getNext(),

print ''
print '=',
for i in range(0, 26):
    print r.getPrevious(),