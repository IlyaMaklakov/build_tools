#!/usr/bin/env python

import config
import base

def make():
  base_dir = base.get_script_dir() + "/../out"
  git_dir = base.get_script_dir() + "/../.."
  core_dir = git_dir + "/core"
  branding = config.branding()

  platforms = config.option("platform").split()
  for native_platform in platforms:
    if not native_platform in config.platforms:
      continue

    root_dir = base_dir + ("/" + native_platform + "/" + branding + "/mobile"
    if (base.is_dir(root_dir)):
      base.delete_dir(root_dir)
    base.create_dir(root_dir)

    qt_dir = base.qt_setup(native_platform)
    platform = native_platform

    core_build_dir = core_dir + "/build"
    if ("" != config.option("branding")):
      core_build_dir += ("/" + config.option("branding"))

    platform_postfix = platform + base.qt_dst_postfix()

    # x2t
    base.copy_lib(core_build_dir + "/lib/" + platform_postfix, root_dir, "kernel")
    base.copy_lib(core_build_dir + "/lib/" + platform_postfix, root_dir, "UnicodeConverter")
    base.copy_lib(core_build_dir + "/lib/" + platform_postfix, root_dir, "graphics")
    base.copy_lib(core_build_dir + "/lib/" + platform_postfix, root_dir, "PdfWriter")
    base.copy_lib(core_build_dir + "/lib/" + platform_postfix, root_dir, "PdfReader")
    base.copy_lib(core_build_dir + "/lib/" + platform_postfix, root_dir, "DjVuFile")
    base.copy_lib(core_build_dir + "/lib/" + platform_postfix, root_dir, "XpsFile")
    base.copy_lib(core_build_dir + "/lib/" + platform_postfix, root_dir, "HtmlFile")
    base.copy_lib(core_build_dir + "/lib/" + platform_postfix, root_dir, "HtmlRenderer")
    base.copy_lib(core_build_dir + "/lib/" + platform_postfix, root_dir, "doctrenderer")

    if ("ios" == platform) or (0 == platform.find("android")):
      base.copy_lib(core_build_dir + "/lib/" + platform_postfix, root_dir, "x2t")
    else:
      base.copy_exe(core_build_dir + "/bin/" + platform_postfix, root_dir, "x2t")

    # icu
    if (0 == platform.find("win")):
      base.copy_file(core_dir + "/Common/3dParty/icu/" + platform + "/build/icudt58.dll", root_dir + "/icudt58.dll")
      base.copy_file(core_dir + "/Common/3dParty/icu/" + platform + "/build/icuuc58.dll", root_dir + "/icuuc58.dll")

    if (0 == platform.find("linux")):
      base.copy_file(core_dir + "/Common/3dParty/icu/" + platform + "/build/libicudata.so.58", root_dir + "/libicudata.so.58")
      base.copy_file(core_dir + "/Common/3dParty/icu/" + platform + "/build/libicuuc.so.58", root_dir + "/libicuuc.so.58")

    if (0 == platform.find("mac")):
      base.copy_file(core_dir + "/Common/3dParty/icu/" + platform + "/build/libicudata.58.dylib", root_dir + "/libicudata.58.dylib")
      base.copy_file(core_dir + "/Common/3dParty/icu/" + platform + "/build/libicuuc.58.dylib", root_dir + "/libicuuc.58.dylib")

    # app
    base.generate_doctrenderer_config(root_dir + "/DoctRenderer.config", "./", "builder")
    base.copy_dir(git_dir + "/DocumentBuilder/empty", root_dir + "/empty")
    
    # js
    base.copy_dir(base_dir + "/js/" + branding + "/mobile/sdkjs", root_dir + "/sdkjs")

    # correct ios frameworks
    if ("ios" == platform):
      base.generate_plist(root_dir)

    if (0 == platform.find("mac")):
      base.mac_correct_rpath_x2t(root_dir)
  return
