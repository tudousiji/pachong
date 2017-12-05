import traceback

try:
    aa = 1
    aa / 0
except Exception as e:

    print("str(Exception):\t", str(Exception))
    print("str(e):\t\t", str(e))
    print("repr(e):\t", repr(e))
    # print("e.message:\t", e.message)
    print("traceback.print_exc():");
    print(traceback.print_exc());
    print("traceback.format_exc():\n%s" % traceback.format_exc())
