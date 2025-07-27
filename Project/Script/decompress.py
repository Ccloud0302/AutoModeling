# 导入必要的库
import lz4.block
import binascii

# 读取并尝试解压文件
file_path = 'C:\\Users\\shiha\\OneDrive - mail.sdu.edu.cn\\Desktop\\trid_w32\\script_compressed_kor_4_4_u_p(1).bytes'

# 由于文件可能是二进制压缩格式，尝试直接解压看看是否成功
with open(file_path, 'rb') as f:
    byte = f.read(1)
    hexadecimal = binascii.hexlify(byte)
    decimal = int(hexadecimal, 16)
    binary = bin(int(binascii.hexlify(byte), 16))[2:].zfill(8)
    print("hex: %s, decimal: %s, binary: %s" % (hexadecimal, decimal, binary))

# 使用 lz4.frame.decompress 进行解压
# decompressed_data, _ = lz4.frame.decompress(compressed_data)  # 注意提取第一个元素

#
# with open("output_file", "wb") as f_out:
#     f_out.write(decompressed_data)