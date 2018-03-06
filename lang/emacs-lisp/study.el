;;; study.el --- elisp study file

;; setq 设置变量
(setq name "rgb-24bit" email "rgb-24bit@foxmail.com")

;; concat 连接字符串
(concat name email)

;; load-file-name 加载的文件名(包含路径)， file-name-directory 分离出文件所在的目录
(file-name-directory "~/.emacs.d/init.el")

;; load-file 加载文件
(load-file "file_name.el")

