class Animation:
    def __init__(self,images,frameTime,subAnimations:dict,masterImageid,shadow_imgs,sub_shadow_imgs):
        self.frametime = frameTime
        self.masterImageid = masterImageid
        self.images = images
        self.index = 0
        self.shadow_imgs = shadow_imgs
        self.sub_shadow_imgs = sub_shadow_imgs
        self.len=len(images)
        self.counter = 0
        self.loop_sub=False
        self.sub_remain_loop_times=0

        self.curant_sub_animation_name=None
        self.subAnimations = subAnimations
        self.current_subAnimation =None
    def getImage(self):
        if self.current_subAnimation:
            return self.getSubAnimation()
        self.counter+=1
        if self.counter >= self.frametime:
            self.counter = 0
            self.index+=1
        if self.index >= self.len:
            self.index = 0

        return self.images[self.index]
    def getRenderLoopId(self):
        return self.masterImageid
    def getSurface(self):
        return self.images[0]
    def play(self,name):
        self.curant_sub_animation_name=name
        self.loop_sub=False
        self.subAnimation_counter=0
        self.subAnimation_index=0
        self.subAnimation_len=len(self.subAnimations[name]["imgs"])
        self.current_subAnimation = self.subAnimations[name]
    def get_width(self):
        return self.images[0].get_width()
    def get_height(self):
        return self.images[0].get_height()

    def loop(self,name,times=1):
        if self.curant_sub_animation_name==name:
            self.sub_remain_loop_times=times
            return
        self.curant_sub_animation_name = name
        self.loop_sub = True
        self.sub_remain_loop_times = times
        self.subAnimation_counter = 0
        self.subAnimation_index = 0
        self.subAnimation_len = len(self.subAnimations[name])
        self.current_subAnimation = self.subAnimations[name]

    def getShadow_img(self):
        if self.current_subAnimation:
            return self.sub_shadow_imgs[self.curant_sub_animation_name][self.subAnimation_index]
        return self.shadow_imgs[self.index]
    def getSubAnimation(self):
        self.subAnimation_counter+=1
        self.sub_remain_loop_times -= 1
        if self.subAnimation_counter >= self.current_subAnimation["delay"]:
            self.subAnimation_counter = 0

            self.subAnimation_index+=1
        if (self.subAnimation_index >= self.subAnimation_len)|(self.sub_remain_loop_times==0):
            if (not self.loop_sub)|(self.sub_remain_loop_times==0):
                self.current_subAnimation=None
                self.sub_remain_loop_times=0
                self.curant_sub_animation_name=None
                return self.getImage()
            else:
                self.subAnimation_index=0

        print(self.subAnimation_index,self.subAnimation_len)

        return self.current_subAnimation["imgs"][self.subAnimation_index]

