

s = "123456789"


def count(number, offset, gs, record):
    if offset == 9:
        if number == 50:
            print(gs, record)
        return
    for num in range(1, 6):
        if num == 1:
            count(number + float(s[offset:offset+1]), offset +
                  1, gs + '+%d' % float(s[offset: offset+1]), record + "\n当前第%d步 加法  %d + %d = %d" % (offset, number, float(s[offset:offset+1]), number + float(s[offset:offset+1])))
        elif num == 2:
            count(number - float(s[offset:offset+1]), offset +
                  1, gs + '-%d' % float(s[offset:offset+1]), record + "\n当前第%d步 减法  %d - %d = %d" % (offset, number, float(s[offset:offset+1]), number - float(s[offset:offset+1])))
        elif num == 3:
            count(number * float(s[offset:offset+1]), offset +
                  1, gs + '*%d' % float(s[offset:offset+1]), record + "\n当前第%d步 乘法  %d * %d = %d" % (offset, number, float(s[offset:offset+1]), number * float(s[offset:offset+1])))
        elif num == 4:
            count(number / float(s[offset:offset+1]), offset +
                  1, gs + '/%d' % float(s[offset:offset+1]), record + "\n当前第%d步 除法  %d / %d = %d" % (offset, number, float(s[offset:offset+1]), number / float(s[offset:offset+1])))
        elif num == 5:
            # 上一步已经算过了,所以这部要撤回,分5种情况
            for t in range(1, 6):
                if t == 1:
                    n = number - float(s[offset-1:offset])
                    count(n*10 + float(s[offset:offset+1]), offset +
                          1, gs + '%d' % float(s[offset:offset+1]), record + "\n当前第%d步 合并 先把上一步回退得到 %d  %d * 10 + %d = %d" % (offset, n, n, float(s[offset:offset+1]), n*10 + float(s[offset:offset+1])))
                elif t == 2:
                    n = number + float(s[offset-1:offset])
                    count(n*10 + float(s[offset:offset+1]), offset +
                          1, gs + '%d' % float(s[offset:offset+1]), record + "\n当前第%d步 合并 先把上一步回退得到 %d  %d * 10 + %d = %d" % (offset, n, n, float(s[offset:offset+1]), n*10 + float(s[offset:offset+1])))
                elif t == 3:
                    n = number / float(s[offset-1:offset])
                    count(n*10 + float(s[offset:offset+1]), offset +
                          1, gs + '%d' % float(s[offset:offset+1]), record + "\n当前第%d步 合并 先把上一步回退得到 %d  %d * 10 + %d = %d" % (offset, n, n, float(s[offset:offset+1]), n*10 + float(s[offset:offset+1])))
                elif t == 4:
                    n = number * float(s[offset-1:offset])
                    count(n*10 + float(s[offset:offset+1]), offset +
                          1, gs + '%d' % float(s[offset:offset+1]), record + "\n当前第%d步 合并 先把上一步回退得到 %d  %d * 10 + %d = %d" % (offset, n, n, float(s[offset:offset+1]), n*10 + float(s[offset:offset+1])))


count(1, 1, '1', '')
