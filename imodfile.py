import struct
from typing import List, Tuple, Dict, Any


class IMODModel:
    def __init__(self):
        self.name: str = ""
        self.xmax: int = 0
        self.ymax: int = 0
        self.zmax: int = 0
        self.objsize: int = 0
        self.flags: int = 0
        self.drawmode: int = 0
        self.mousemode: int = 0
        self.blacklevel: int = 0
        self.whitelevel: int = 0
        self.xoffset: float = 0.0
        self.yoffset: float = 0.0
        self.zoffset: float = 0.0
        self.xscale: float = 0.0
        self.yscale: float = 0.0
        self.zscale: float = 0.0
        self.object: int = 0
        self.contour: int = 0
        self.point: int = 0
        self.res: int = 0
        self.thresh: int = 0
        self.pixsize: float = 0.0
        self.units: int = 0
        self.csum: int = 0
        self.alpha: float = 0.0
        self.beta: float = 0.0
        self.gamma: float = 0.0
        self.objects: List["IMODObject"] = []
        self.optional_chunks: List[Dict[str, Any]] = []


class IMODObject:
    def __init__(self):
        self.name: str = ""
        self.extra: bytes = b""
        self.contsize: int = 0
        self.flags: int = 0
        self.axis: int = 0
        self.drawmode: int = 0
        self.red: float = 0.0
        self.green: float = 0.0
        self.blue: float = 0.0
        self.pdrawsize: int = 0
        self.symbol: int = 0
        self.symsize: int = 0
        self.linewidth2: int = 0
        self.linewidth: int = 0
        self.linesty: int = 0
        self.symflags: int = 0
        self.sympad: int = 0
        self.trans: int = 0
        self.meshsize: int = 0
        self.surfsize: int = 0
        self.contours: List["IMODContour"] = []
        self.meshes: List["IMODMesh"] = []
        self.optional_chunks: List[Dict[str, Any]] = []


class IMODContour:
    def __init__(self):
        self.psize: int = 0
        self.flags: int = 0
        self.time: int = 0
        self.surf: int = 0
        self.points: List[Tuple[float, float, float]] = []
        self.optional_chunks: List[Dict[str, Any]] = []


class IMODMesh:
    def __init__(self):
        self.vsize: int = 0
        self.lsize: int = 0
        self.flag: int = 0
        self.time: int = 0
        self.surf: int = 0
        self.vertices: List[Tuple[float, float, float]] = []
        self.indices: List[int] = []
        self.optional_chunks: List[Dict[str, Any]] = []


def parse_imod(file_path: str) -> IMODModel:
    """Parse an IMOD file and return an IMODModel object."""
    model = IMODModel()
    with open(file_path, "rb") as f:
        # Read IMOD header (8 bytes)
        imod_id = f.read(4)
        version = f.read(4)
        if imod_id != b"IMOD" or version != b"V1.2":
            raise ValueError("Invalid IMOD file format or version.")

        # Read model header (232 bytes)
        model_header = f.read(232)
        fmt = ">128s3iI4i3f3f3i2ifii3f"
        fields = struct.unpack(fmt, model_header)
        model.name = fields[0].decode("latin-1").strip("\x00")
        model.xmax, model.ymax, model.zmax = fields[1], fields[2], fields[3]
        model.objsize = fields[4]
        model.flags = fields[5]
        model.drawmode, model.mousemode = fields[6], fields[7]
        model.blacklevel, model.whitelevel = fields[8], fields[9]
        model.xoffset, model.yoffset, model.zoffset = fields[10], fields[11], fields[12]
        model.xscale, model.yscale, model.zscale = fields[13], fields[14], fields[15]
        model.object, model.contour, model.point = fields[16], fields[17], fields[18]
        model.res, model.thresh = fields[19], fields[20]
        model.pixsize = fields[21]
        model.units = fields[22]
        model.csum = fields[23]
        model.alpha, model.beta, model.gamma = fields[24], fields[25], fields[26]

        # Read objects
        for _ in range(model.objsize):
            obj = IMODObject()
            obj_id = f.read(4)
            if obj_id != b"OBJT":
                raise ValueError("Expected OBJT chunk.")
            obj_data = f.read(176)
            obj_fmt = ">64s64s i I i i 3f i 8B ii"
            obj_fields = struct.unpack(obj_fmt, obj_data)
            obj.name = obj_fields[0].decode("latin-1").strip("\x00")
            obj.extra = obj_fields[1]
            obj.contsize = obj_fields[2]
            obj.flags = obj_fields[3]
            obj.axis = obj_fields[4]
            obj.drawmode = obj_fields[5]
            obj.red, obj.green, obj.blue = obj_fields[6], obj_fields[7], obj_fields[8]
            obj.pdrawsize = obj_fields[9]
            (
                obj.symbol,
                obj.symsize,
                obj.linewidth2,
                obj.linewidth,
                obj.linesty,
                obj.symflags,
                obj.sympad,
                obj.trans,
            ) = obj_fields[10:18]
            obj.meshsize, obj.surfsize = obj_fields[18], obj_fields[19]

            # Read contours
            for _ in range(obj.contsize):
                cont = IMODContour()
                cont_id = f.read(4)
                if cont_id != b"CONT":
                    raise ValueError("Expected CONT chunk.")
                cont_header = f.read(16)
                psize, flags, time, surf = struct.unpack(">i I i i", cont_header)
                cont.psize = psize
                cont.flags = flags
                cont.time = time
                cont.surf = surf
                points_data = f.read(12 * psize)
                cont.points = [
                    struct.unpack(">3f", points_data[i * 12 : i * 12 + 12])
                    for i in range(psize)
                ]
                obj.contours.append(cont)

            # Read meshes
            for _ in range(obj.meshsize):
                mesh = IMODMesh()
                mesh_id = f.read(4)
                if mesh_id != b"MESH":
                    raise ValueError("Expected MESH chunk.")
                mesh_header = f.read(20)
                vsize, lsize, flag, time, surf = struct.unpack(
                    ">i i I h h", mesh_header
                )
                mesh.vsize = vsize
                mesh.lsize = lsize
                mesh.flag = flag
                mesh.time = time
                mesh.surf = surf
                vert_data = f.read(12 * vsize)
                mesh.vertices = [
                    struct.unpack(">3f", vert_data[i * 12 : i * 12 + 12])
                    for i in range(vsize)
                ]
                list_data = f.read(4 * lsize)
                mesh.indices = struct.unpack(f">{lsize}i", list_data)
                obj.meshes.append(mesh)

            # Read optional chunks for the object
            while True:
                chunk_pos = f.tell()
                chunk_id = f.read(4)
                if not chunk_id:
                    break
                if chunk_id in (b"OBJT", b"IEOF"):
                    f.seek(chunk_pos)
                    break
                size = struct.unpack(">I", f.read(4))[0]
                data = f.read(size)
                obj.optional_chunks.append({"id": chunk_id, "data": data})

            model.objects.append(obj)

        # Read model optional chunks and IEOF
        while True:
            chunk_id = f.read(4)
            if not chunk_id:
                break
            if chunk_id == b"IEOF":
                break
            size = struct.unpack(">I", f.read(4))[0]
            data = f.read(size)
            model.optional_chunks.append({"id": chunk_id, "data": data})

    return model


def write_imod(model: IMODModel, file_path: str) -> None:
    """Write an IMODModel object to a file."""
    with open(file_path, "wb") as f:
        # Write IMOD header
        f.write(b"IMODV1.2")

        # Write model header
        model_fmt = ">128s3iI4i3f3f3i2ifii3f"
        name = model.name.encode("latin-1")[:128].ljust(128, b"\x00")
        fields = (
            name,
            model.xmax,
            model.ymax,
            model.zmax,
            model.objsize,
            model.flags,
            model.drawmode,
            model.mousemode,
            model.blacklevel,
            model.whitelevel,
            model.xoffset,
            model.yoffset,
            model.zoffset,
            model.xscale,
            model.yscale,
            model.zscale,
            model.object,
            model.contour,
            model.point,
            model.res,
            model.thresh,
            model.pixsize,
            model.units,
            model.csum,
            model.alpha,
            model.beta,
            model.gamma,
        )
        packed = struct.pack(model_fmt, *fields)
        f.write(packed)

        # Write objects
        for obj in model.objects:
            f.write(b"OBJT")
            obj_name = obj.name.encode("latin-1")[:64].ljust(64, b"\x00")
            obj_fmt = ">64s64s i I i i 3f i 8B ii"
            fields = (
                obj_name,
                obj.extra,
                obj.contsize,
                obj.flags,
                obj.axis,
                obj.drawmode,
                obj.red,
                obj.green,
                obj.blue,
                obj.pdrawsize,
                obj.symbol,
                obj.symsize,
                obj.linewidth2,
                obj.linewidth,
                obj.linesty,
                obj.symflags,
                obj.sympad,
                obj.trans,
                obj.meshsize,
                obj.surfsize,
            )
            packed = struct.pack(obj_fmt, *fields)
            f.write(packed)

            # Write contours
            for contour in obj.contours:
                f.write(b"CONT")
                header = struct.pack(
                    ">i I i i", contour.psize, contour.flags, contour.time, contour.surf
                )
                f.write(header)
                for point in contour.points:
                    f.write(struct.pack(">3f", *point))

            # Write meshes
            for mesh in obj.meshes:
                f.write(b"MESH")
                header = struct.pack(
                    ">i i I h h",
                    mesh.vsize,
                    mesh.lsize,
                    mesh.flag,
                    mesh.time,
                    mesh.surf,
                )
                f.write(header)
                for vertex in mesh.vertices:
                    f.write(struct.pack(">3f", *vertex))
                f.write(struct.pack(f">{mesh.lsize}i", *mesh.indices))

            # Write optional chunks for object
            for chunk in obj.optional_chunks:
                f.write(chunk["id"])
                f.write(struct.pack(">I", len(chunk["data"])))
                f.write(chunk["data"])

        # Write model optional chunks
        for chunk in model.optional_chunks:
            f.write(chunk["id"])
            f.write(struct.pack(">I", len(chunk["data"])))
            f.write(chunk["data"])

        # Write IEOF
        f.write(b"IEOF")


# Example usage:
if __name__ == "__main__":
    # Read an IMOD model
    model = parse_imod("input.mod")

    # Modify the model if needed
    model.name = "Modified Model"

    # Write the modified model
    write_imod(model, "output.mod")
