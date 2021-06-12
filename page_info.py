from page_structure import FileHeader as FH, PageHeader as PH, VirtualRecord as VR
from print_strategy import count_the_index_and_record_num as count, print_index_and_record_num as piar, print_tree_level, count_tree_slot, print_index_and_record_slot
import optparse
import os
from idb import analysis,fileformat,idapython



INNODB_PAGE_SIZE = 0


def print_btree_detail(filename):
    ibd_file = open(filename, 'rb')
    ibd_file_size = os.path.getsize(filename)
    total_page = ibd_file_size / INNODB_PAGE_SIZE
    print("the idb file contains %d pages" % total_page)
    while total_page > 0:
        page = ibd_file.read(INNODB_PAGE_SIZE)
        # 统计索引数和行记录数
        print_tree_level(page, FH.FIL_PAGE_TYPE, PH.PAGE_LEVEL)
        count(page, FH.FIL_PAGE_TYPE, PH.PAGE_N_RECS, VR.PAGE_SUPREMUM)
        count_tree_slot(page, FH.FIL_PAGE_TYPE, PH.PAGE_N_DIR_SLOTS, VR.PAGE_SUPREMUM)
        ###
        total_page = total_page - 1
    piar()
    print_index_and_record_slot()



if __name__ == '__main__':
    parser = optparse.OptionParser(usage="page_info.py [options] filename")
    parser.add_option("--page-size", dest="page_size", default=16, type=int, help="set page size, default 16KB")
    parser.add_option("-p", dest="print_")
    parser.add_option("-s", dest="skip", default=0, type=int, help="skip bytes")
    parser.add_option("-n", dest="length", default=0, type=int, help="bytes length")
    (options, args) = parser.parse_args()
    INNODB_PAGE_SIZE = options.page_size * 1024
    print_btree_detail(args[0])