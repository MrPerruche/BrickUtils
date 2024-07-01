import brci
from data import char_blacklist, multi_replace


def return_matches(prompt: list[str]) -> list[str]:

    bricks: list[str] = list(brci.br_brick_list.keys())
    bricks.remove('default_brick_data')

    fixed_bricks: list[str] = []
    for brick in bricks:
        fixed_bricks.append(multi_replace(brick, char_blacklist, '').lower())

    fixed_prompt: list[str] = []
    for word in prompt:
        fixed_prompt.append(multi_replace(word, char_blacklist, '').lower())

    if not prompt: # prompt == []
        return bricks
    # else:

    matches: list[str] = []

    # O(n^2) brother ew brother whats that ik ik but guess what I'm lazy it's only gonna do like 8,000 iterations at worst eitherway
    for i, fixed_brick in enumerate(fixed_bricks):
        is_inside: list[bool] = []
        for word in fixed_prompt:
            is_inside.append(word in fixed_brick)
        if all(is_inside):
            matches.append(bricks[i])

    return matches


def get_brick_properties(brick: str) -> dict[str, any]:

    if brick in brci.br_brick_list:
        return brci.create_brick(brick)

    # else:
    return {}