from bs4 import BeautifulSoup as bs


def get_isbn_publisher():
    pub_no_list = (
        {
            "keta": 2,
            "start": 0,
            "end": 19
        },
        {
            "keta": 3,
            "start": 250,
            "end": 699
        },
        {
            "keta": 4,
            "start": 7500,
            "end": 8499
        },
        {
            "keta": 5,
            "start": 86000,
            "end": 89999
        },
        {
            "keta": 6,
            "start": 900000,
            "end": 949999
        },
        {
            "keta": 7,
            "start": 9900000,
            "end": 9999999
        }
    )

    pub_no_list = (
        {
            "keta": 2,
            "start": 0,
            "end": 19
        },
    )

    for kse in pub_no_list:
        keta = kse["keta"]
        start = kse["start"]
        end = kse["end"]

        for n in range(start, end+1):   # endの最後の数字も使うから+1
            cur_pub_no = f"{n:0{keta}}"
            get_one_publisher(cur_pub_no)

    return pub_no_list


def get_one_publisher(pub_no):
    
    return
