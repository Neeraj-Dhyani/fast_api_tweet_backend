
import os
import uuid
import shutil
from PIL import Image, UnidentifiedImageError


def save_the_file(file, username):
    image = Image.open(file.file)
    try:
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")
                    
        image = image.resize((256, 256))

        user_folder = os.path.join("uploads", username)
        os.makedirs(user_folder, exist_ok=True)
        avatar = os.path.join(user_folder, "avatar")
        os.makedirs(avatar, exist_ok=True)

        unique_filename = f"{uuid.uuid4()}.png"
            
        file_path = os.path.join(avatar, unique_filename)
            
        image.save(file_path, format="PNG")

    except UnidentifiedImageError as err:
        return {"status_code":400, "detail":f"Invalid image file uploaded. {err}"}

    # 4. Generate URL and save to database
    image_url = f"/static/{username}/avatar/{unique_filename}"
    return image_url


def update_the_file(file, source):
    image = Image.open(file.file)
    if image.mode in ("RGBA", "P"):
                image = image.convert("RGB")
                        
    image = image.resize((256, 256))
    try:
        dir_name = source.split("/static",1)[1]
       
        search_dir = "./uploads"

        old_file = os.path.join(search_dir, dir_name.lstrip("/"))
       
        image.save(old_file, format="PNG")
        

    except UnidentifiedImageError as err:
        return {"status_code":400, "detail":f"Invalid image file uploaded. {err}"}


    image_url = source
    return image_url

def remove_user_avatar(avatar_path:str):
    try:
        terget_dir = avatar_path.split("/static/")[1]
        main_dir = "./uploads"
        
        path = os.path.join(main_dir, terget_dir)
        if not os.path.isfile(path):
             return{
                  "success":False,
                  "message":"User Avatar File Not Found!",
                  "path":path
             }   
            
        os.remove(path)

        return {
             "success":True,
             "message":"Avatar Successfully Removed!"
        }
    except OSError as  err:
         print(err)
         return {
                "success":False,
                "message":"Error"
            }
    

def delete_user_asset(usename_path):
    try:
        main_dir = "./uploads"
        dir = usename_path
        path = os.path.join(main_dir, dir)
        shutil.rmtree(path)
        # print("% s removed successfully" % path)
        return {
             "success":True
        }
    except OSError as error:
        # print(error)
        return {
            "success":False,
            "error":error,
            "path":usename_path
        }

def save_multiple_file(files, username, post_time):
    images_url = []
    mode = []
    try:
        root_dir = './uploads'
        user_path = os.path.join(root_dir, username)

        user_post_path = os.path.join(user_path, "user_post")
        os.makedirs(user_post_path, exist_ok=True)

        user_post_file_path = os.path.join(user_post_path, post_time)
        os.makedirs(user_post_file_path, exist_ok=True)

        for file in files:
            image = Image.open(file.file)
            mode.append(image.mode)
            if image.mode == "RGBA":
                image = image.convert("RGB")

            unique_file_name = f"{uuid.uuid1()}.jpg"

            file_path = os.path.join(user_post_file_path, unique_file_name)

            image.save(file_path, format="JPEG", optimize=True, quality=80)
            split_path = os.path.relpath(file_path, root_dir)
            static_path = "/static/"+split_path.replace(os.sep ,"/")
            images_url.append(static_path)

        return {
             "success":True,
             "images":images_url
        }

    except OSError as error:
            return {
              "success":False,
              "error":str(error),
              "mode":mode
         }


def delete_user_post(paths):
    try:
       
        for path in paths:
            split_path = path.split("/static/")[1]
            terget_dir = os.path.dirname(split_path)
            root_dir = "./uploads"
            path_dir = os.path.join(root_dir, terget_dir)

            print (path_dir)
            if not os.path.isdir(path_dir):
                 return{
                    "success":False,
                    "message":"User Post File Not Found!",
                    "path":path
                    } 

            shutil.rmtree(path_dir)
              
    except OSError as error:
          return {
               "success":False,
               "error":str(error)
          }

