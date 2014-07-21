function range(start,end){
    var list = [];
    if(start >= end) return [start];
    for(var i = start;i < end; i++){
        list.push(i);
    }
    return list;
}

function shuffle(o){
    for(var j, x, i = o.length; i; j = Math.floor(Math.random() * i), x = o[--i], o[i] = o[j], o[j] = x);
    return o;
}
/*
//ID序列
function IdList(){}

IdList.prototype.addNum = function(){};
IdList.prototype.removeNum = function(){};
IdList.prototype.current = function(){};
IdList.prototype.go = function(){};
IdList.prototype.getNext = function(){};
IdList.prototype.goNext = function(){};
IdList.prototype.getPrevious = function(){};
IdList.prototype.goPrevious = function(){};
//顺序序列
function OrderedIdList(nums, firstnum){
    this.nums = nums;  //列表长度
    this.current = firstnum; //当前指针位置
}
OrderedIdList.prototype.addNum = function(){
};
OrderedIdList.prototype.removeNum = function(){};
OrderedIdList.current = function(){
    return this.current;
};
OrderedIdList.prototype.go = function(num){
    this.current = num;
};
OrderedIdListprototype..getNext = function(){
    if(this.nums == 0)  return undefined;
    if(!this.current) return 0;
    return (this.current + 1) % this.nums;
};
OrderedIdList.prototype.goNext = function(){
    return this.current = this.getNext();
};
OrderedIdList.getPrevious = function(){
    if(this.nums == 0) return undefined;
    if(!this.current) return this.nums - 1;
    return (this.current + this.nums - 1)% this.nums
};
OrderedIdList.goPrevious = function(){
    return this.current = this.getPrevious();
};
*/
//随机播放列表（下面以12345这5首歌为例，-表示序列后面的数字是前进播放，=表示序列后面的数字是回退操作）
//a. 前进时发现无数据，将生产一个随机序列，生产的随机队列第一个数字不上个序列最后一个数字相同
//        从空列表开始 -24513，播放到3时 -54231， -24
//b. 回退将回溯到之前的播放，将保存上一次的播放序列保证回溯操作的连贯性
//        从之前4回退， =2 =13245
//c. 回退到播放历史不存在的时候仍回退将在最后一个序列中无限循环
//        继续回退，=13245 =13
//d. 回退后的前进操作将先按之前的播放序列继续播放
//    前进-1 -54231 -24……
//thread not safe, invoke in UI thread ！！

function RandomIdList(nums, firstnum){
    this.lists = [];      //随机列表队列，每项都是一个随机播放列表
    this.addOneList(nums, firstnum);
    this.nums = nums;
    this.idxx = 0;
    this.idxy = nums?0:undefined;//TODO:需要加东西
    this.previousRepeatFirstList = false;
}
RandomIdList.prototype.addNum = function(){};
RandomIdList.prototype.removeNum = function(){};
RandomIdList.prototype.current = function(){
    return this.get(this.idxx, this.idxy);
};

RandomIdList.prototype.get = function(idxx, idxy){

    if(idxy==undefined){return undefined;}
    return this.lists[idxx][idxy];
};

RandomIdList.prototype.addNum = function(nums){

};

RandomIdList.prototype.removeNum = function(){

};




RandomIdList.prototype.getNext = function(){
    if(this.lists[this.lists.length - 1].length == 0){
        return;
    }
    var idxx = this.idxx;
    var idxy = (this.idxy!=undefined)?(this.idxy + 1): 0;
    var finishPreviousRepeatFirstList = false;
    if(idxy >= this.lists[this.idxx].length){
        if(this.previousRepeatFirstList){
            idxx = 0;
            finishPreviousRepeatFirstList = true
        }else{
            idxx = this.idxx + 1;
            idxy = 0;
            if(idxx == this.lists.length){
                this.addOneList(this.lists[idxx - 1].length);
            }
        }
    }
    return {
        idxx: idxx,
        idxy: idxy,
        fprfl: finishPreviousRepeatFirstList
    }
};
RandomIdList.prototype.goNext = function(){
    var getNext = this.getNext();
    this.idxx = getNext.idxx;
    this.idxy = getNext.idxy;
    var finishPreviousRepeatFirstList = getNext.fprfl;

    if(this.lists.length == 3 && this.idxx > 0){
        this.lists.splice(0,1);
        this.idxx = this.idxx -1;
    }
    if(!!finishPreviousRepeatFirstList){
        this.previousRepeatFirstList = false;
    }
    return this.current()
};

RandomIdList.prototype.getPrevious = function(){
    if(this.lists[this.lists.length - 1].length == 0)   return;
    var idxx = this.idxx;
    var idxy = (this.idxy!=undefined)?(this.idxy-1):(-1);

    var repeatFirstList = false;

    if(idxy == -1){
        idxx = idxx -1;
        if(idxx = -1){
            idxx = 0;
            repeatFirstList = true
        }
        idxy = this.lists[idxx].length - 1;
    }
    return {
        idxx:idxx,
        idxy:idxy,
        repeatFirstList:repeatFirstList
    }
};

RandomIdList.prototype.goPrevious = function(){
    var getPrevious = this.getPrevious();
    this.idxx = getPrevious.idxx;
    this.idxy = getPrevious.idxy;
    var repeatFirstList = getPrevious.repeatFirstList;

    if(repeatFirstList)
        this.previousRepeatFirstList = true;

    return this.current();
};



//添加一个num场的随机序列
RandomIdList.prototype.addOneList = function(nums, firstnum){
    var lastnum = -1;
    if(this.lists.length != 0){
        var lastlist = this.lists[this.lists.length - 1];
        lastnum = lastlist[lastlist.length - 1];
    }
    this.lists.push(this.genRandIds(nums, lastnum));
};
//生成随机ID 列表,使得第一个数字是firstnum,不是notfirstnum(当队列长度大于1的时候)
RandomIdList.prototype.genRandIds = function(nums, notfirstnum, firstnum){
    var randomIds = range(0, nums);
    shuffle(randomIds);
    if(randomIds[0] != firstnum && nums != 1 && firstnum!=undefined){
        var toswitch = randomIds.indexOf(firstnum);
        var temp = randomIds[toswitch];
        randomIds[toswitch] = randomIds[0];
        randomIds[0] = temp;
    }
    if(randomIds[0] == notfirstnum && nums != 1 && notfirstnum!=undefined){
        var toswitch = 1 + Math.floor(Math.random() * (nums - 2));
        var temp = randomIds[toswitch];
        randomIds[toswitch] = randomIds[0];
        randomIds[0] = temp;
    }
    return randomIds;
};






