import pandas as pd

check_domain_size = 2  # 测试域大小，只要测试点值比周围2n+1*2n+1的点都大，则记为有效高值
highest_points_number = 3  # 输出高值点个数

# reshape 并排序，返回的index为tuple，第一个值为原本行号，第二个值为原本列名
def reshape_and_sort(reshape_input_df):
    stacked_df = reshape_input_df.stack()
    sorted_df = stacked_df.sort_values(ascending=False)
    return sorted_df

# 依据中心点index与测试域大小划定切割测试域，正常测试域大小为2n+1*2n+1，当位于边界处时将会小于2n+1*2n+1
def cut_check_domain(cut_input_df, point_index_tuple, size_int):
    raw = point_index_tuple[0]
    column = point_index_tuple[1]
    raw_min = raw - size_int
    raw_max = raw + size_int + 1
    column_min = column - size_int
    column_max = column + size_int + 1
    if raw_min < 0:
        raw_min = 0
    if column_min < 0:
        column_min = 0
    check_domain_df = cut_input_df.iloc[raw_min:raw_max, column_min:column_max]
    return check_domain_df

# 验证所取点是否为有效高值
def validity_check(validity_input_df, point_index_tuple, size_int):
    check_domain_df = cut_check_domain(
        validity_input_df, point_index_tuple, size_int)
    reshape_and_sort_df = reshape_and_sort(check_domain_df)
    highest_point_on_check_domain = reshape_and_sort_df.index[0]
    if highest_point_on_check_domain == point_index_tuple:
        validity = 'DDF'
    else:
        validity = 'NEXT'
    return validity


def find_the_highest_value(find_input_df, size_int, points_num):
    highest_points_count = 0  # 高值点计数
    highest_points = []  # 存放结果
    sorted_df = reshape_and_sort(find_input_df)
    for i in range(len(sorted_df)):
        max_tuple = sorted_df.index[i]
        validity_result = validity_check(find_input_df, max_tuple, size_int)
        if validity_result == 'DDF':
            point_information = {
                'value': sorted_df[max_tuple], 'lon': max_tuple[0], 'lat': max_tuple[1]}
            highest_points = [*highest_points, point_information]
            highest_points_count = highest_points_count + 1
        if highest_points_count == points_num:
            break

    return highest_points


if __name__ == '__main__':
    test_df = pd.read_csv('test.csv', header=None)
    result = find_the_highest_value(test_df, check_domain_size, highest_points_number)
    print(result)
