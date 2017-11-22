from itertools import product

from bag.layout.routing.fill import fill_symmetric_helper


def check_disjoint_union(outer_list, inner_list, start, stop):
    sintv, eintv = outer_list[0], outer_list[-1]
    # test outer list covers more range than inner list
    assert sintv[0] <= inner_list[0][0] and eintv[1] >= inner_list[-1][1]
    # test outer list touches both boundaries
    assert sintv[0] == start and eintv[1] == stop
    # test outer list has 1 more element than inner list
    assert len(outer_list) == len(inner_list) + 1
    # test intervals are disjoint and union is equal to given interval
    for idx in range(len(outer_list)):
        intv1 = outer_list[idx]
        # test interval is non-negative
        assert intv1[0] <= intv1[1]
        if idx < len(inner_list):
            intv2 = inner_list[idx]
            # test interval is non-negative
            assert intv2[0] <= intv2[1]
            # test interval abuts
            assert intv1[1] == intv2[0]
            assert intv2[1] == outer_list[idx + 1][0]


def check_symmetric(intv_list, start, stop):
    # test given interval list is symmetric
    flip_list = [(stop + start - b, stop + start - a) for a, b in reversed(intv_list)]
    for i1, i2 in zip(intv_list, flip_list):
        assert i1[0] == i2[0] and i1[1] == i2[1]


def check_props(fill_list, space_list, num_diff_sp1, num_diff_sp2, n, tot_intv, inc_sp, sp,
                eq_sp_parity, num_diff_sp_max, num_fill, fill_first, start, stop, n_flen_max):
    # check num_diff_sp is the same
    assert num_diff_sp1 == num_diff_sp2
    if n % 2 == eq_sp_parity:
        # check all spaces are the same
        assert num_diff_sp1 == 0
    else:
        # check num_diff_sp is less than or equal to 1
        assert num_diff_sp1 <= num_diff_sp_max
    # test we get correct number of fill
    assert len(fill_list) == num_fill
    # test fill and space are disjoint and union is correct
    if fill_first:
        check_disjoint_union(fill_list, space_list, start, stop)
    else:
        check_disjoint_union(space_list, fill_list, start, stop)
    # check symmetry
    check_symmetric(fill_list, tot_intv[0], tot_intv[1])
    check_symmetric(space_list, tot_intv[0], tot_intv[1])
    # check only two lengths, and they differ by 1
    len_list = sorted(set((b - a) for a, b in fill_list))
    assert len(len_list) <= n_flen_max
    assert (len_list[-1] - len_list[0]) <= n_flen_max - 1
    len_list = sorted(set((b - a) for a, b in space_list))
    assert len(len_list) <= (2 if num_diff_sp1 > 0 else 1)
    assert (len_list[-1] - len_list[0]) <= 1
    # check that space is the right values
    if inc_sp:
        assert len_list[0] == sp
    else:
        assert len_list[-1] == sp


def test_fill_symmetric_non_cyclic():
    # test fill symmetric for non-cyclic
    sp_list = [3, 4, 5]
    inc_sp_list = [True, False]
    offset_list = [0, 4, 7]
    foe_list = [True, False]
    for sp, inc_sp, offset, foe in product(sp_list, inc_sp_list, offset_list, foe_list):
        for area in range(sp + 1, 101):
            tot_intv = offset, offset + area
            for n in range(1, area - sp + 1):
                # get fill and space list
                fill_list, num_diff_sp1 = fill_symmetric_helper(area, n, sp, offset=offset, inc_sp=inc_sp,
                                                                invert=False, fill_on_edge=foe, cyclic=False)
                space_list, num_diff_sp2 = fill_symmetric_helper(area, n, sp, offset=offset, inc_sp=inc_sp,
                                                                 invert=True, fill_on_edge=foe, cyclic=False)

                check_props(fill_list, space_list, num_diff_sp1, num_diff_sp2, n, tot_intv, inc_sp, sp,
                            1, 1, n, foe, tot_intv[0], tot_intv[1], 2)


def test_fill_symmetric_cyclic_edge_fill():
    # test fill symmetric for cyclic, fill on edge
    sp_list = [3, 4, 5]
    inc_sp_list = [True, False]
    offset_list = [0, 4, 7]
    for sp, inc_sp, offset in product(sp_list, inc_sp_list, offset_list):
        for area in range(sp + 1, 101):
            tot_intv = offset, offset + area
            for n in range(1, area - sp + 1):
                # get fill and space list
                fill_list, num_diff_sp1 = fill_symmetric_helper(area, n, sp, offset=offset, inc_sp=inc_sp,
                                                                invert=False, fill_on_edge=True, cyclic=True)
                space_list, num_diff_sp2 = fill_symmetric_helper(area, n, sp, offset=offset, inc_sp=inc_sp,
                                                                 invert=True, fill_on_edge=True, cyclic=True)

                # test boundary fills centers on edge
                sintv, eintv = fill_list[0], fill_list[-1]
                assert (sintv[1] + sintv[0]) % 2 == 0 and (eintv[1] + eintv[0]) % 2 == 0
                assert (sintv[1] + sintv[0]) // 2 == tot_intv[0] and (eintv[1] + eintv[0]) // 2 == tot_intv[1]
                # test other properties
                check_props(fill_list, space_list, num_diff_sp1, num_diff_sp2, n, tot_intv, inc_sp, sp,
                            0, 1, n + 1, True, sintv[0], eintv[1], 3)


def test_fill_symmetric_cyclic_edge_space():
    # test fill symmetric for cyclic, space on edge
    sp_list = [3, 4, 5]
    inc_sp_list = [True, False]
    offset_list = [0, 4, 7]
    for sp, inc_sp, offset in product(sp_list, inc_sp_list, offset_list):
        for area in range(sp + 1, 101):
            tot_intv = offset, offset + area
            for n in range(1, area - sp + 1):
                # get fill and space list
                fill_list, num_diff_sp1 = fill_symmetric_helper(area, n, sp, offset=offset, inc_sp=inc_sp,
                                                                invert=False, fill_on_edge=False, cyclic=True)
                space_list, num_diff_sp2 = fill_symmetric_helper(area, n, sp, offset=offset, inc_sp=inc_sp,
                                                                 invert=True, fill_on_edge=False, cyclic=True)

                # test boundary space centers on edge
                sintv, eintv = space_list[0], space_list[-1]
                assert (sintv[1] + sintv[0]) % 2 == 0 and (eintv[1] + eintv[0]) % 2 == 0
                assert (sintv[1] + sintv[0]) // 2 == tot_intv[0] and (eintv[1] + eintv[0]) // 2 == tot_intv[1]
                # test other properties
                check_props(fill_list, space_list, num_diff_sp1, num_diff_sp2, n, tot_intv, inc_sp, sp,
                            1, 2, n, False, sintv[0], eintv[1], 2)
