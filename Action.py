#!/usr/bin/python3

import os
from pathlib import Path

ADD_PLACE = [
    "C_SOURCES",
    "ifdef GCC_PATH",
    "else",
    "CFLAGS += -MMD",
    "vpath",
    "$(CC) -c $(CFLAGS)",
    "$(SZ) $@",
    "#"*500
]

ADD_STR = [
    "CXX_SOURCES_ = $(wildcard Core/Src/*.cpp) Core/Src/main.cpp\nCXX_SOURCES = $(sort $(CXX_SOURCES_))",
    "CXX = $(GCC_PATH)/$(PREFIX)g++",
    "CXX = $(PREFIX)g++",
    "CXXFLAGS = $(CFLAGS) -fno-rtti -fno-exceptions",
    "OBJECTS += $(addprefix $(BUILD_DIR)/,$(notdir $(CXX_SOURCES:.cpp=.o)))\nvpath %.cpp $(sort $(dir $(CXX_SOURCES)))",
    "$(BUILD_DIR)/%.o: %.cpp Makefile | $(BUILD_DIR) \n\t$(CXX) -c $(CXXFLAGS) -Wa,-a,-ad,-alms=$(BUILD_DIR)/$(notdir $(<:.cpp=.lst)) $< -o $@",
    "$(BUILD_DIR)/$(TARGET).elf: $(OBJECTS) Makefile \n\t$(CXX) $(OBJECTS) $(LDFLAGS) -o $@\n\t$(SZ) $@",
    "#"*500
]

def find_file(root, name):
    files = [i for i in list(root.rglob(name)) if not("Driver" in str(i))]
    if len(files) == 0:
        return None
    if len(files) > 1:
        raise RuntimeError(f"Multiple {name} found: {files}")
    return files[0]

def main():
    warking_dir= Path.cwd().parent

    print("="*10)
    print(warking_dir)
    print("="*10)

    if find_file(warking_dir,"Src/main.cpp") is not None:
        print("start side execute")
        file_name = find_file(warking_dir,"Src/main.cpp")
        os.rename(file_name, Path(str(file_name).replace(".cpp",".c")))

    c_file = find_file(warking_dir,"Src/main.c")
    cpp_path = str(c_file)[len(str(warking_dir)):].replace(".c",".cpp")
    ADD_STR[0] = f"CXX_SOURCES_ = $(wildcard {Path(cpp_path[1:].replace("main","*")).as_posix()}) {Path(str(cpp_path)[1:]).as_posix()}\nCXX_SOURCES = $(sort $(CXX_SOURCES_))"

    if not os.path.exists(warking_dir/"Makefile"):
        print("no Makefile")
        return

    with open(warking_dir/'Makefile', 'r', encoding='utf-8') as f:

        data = ""
        for line in f:
            data += line

        place_iter = iter([pl for pl,i in zip(ADD_PLACE,ADD_STR) if not i in data])
        str_iter = iter([i for i in ADD_STR if not i in data])

        add_place = next(place_iter)
        add_str = next(str_iter)

    file_data = ""

    with open(warking_dir/'Makefile', 'r', encoding='utf-8') as f:
        add_flag = False
        c_source_flag = False
        for line in f:
            if "Src/main.c" in line and c_source_flag:
                if find_file(warking_dir,"Src/main.c") is not None:
                    print("end side execute")
                    file_name = find_file(warking_dir,"Src/main.c")
                    os.rename(file_name,Path(str(file_name).replace(".c",".cpp")))
                continue

            if "Src/main.c" in line:
                index = file_data.rfind("a")
                file_data = file_data[:index] + file_data[index + 1:]
                continue

            if "C_SOURCES" in line:
                c_source_flag = True
            elif not "\\" in line:
                c_source_flag = False
                
            file_data += line

            if line[0] == "#":
                continue

            if add_place in line:
                add_flag = True

            if "\\" in line:
                continue

            if add_flag:
                add_flag = False
                file_data += \
                    "\n#" + "="*10 + "add by Action" + "="*10 + "\n"\
                    + add_str + "\n#" + "="*33 + "\n"
                add_place = next(place_iter)
                add_str = next(str_iter)

    with open(warking_dir/"Makefile", mode='w') as f:
        f.write(file_data)

if __name__ == "__main__":
    main()
