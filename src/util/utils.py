import bisect


@staticmethod
def normalise_dir(dir):
    """Sets all backslashes in an address to forward slashes for neater display"""
    return dir.replace("\\", "/")


@staticmethod
def shorten_dir(dir):
    """Shorten a directory name if it is too long for display"""
    if len(dir) > 65:
        return dir.split("/")[0] + "/........./" + dir.split("/")[-1]

    return dir


def calculate_bill(block_tariff_data, electricity_used):
    """Calculate the final electricity bill"""
    total = 0
    output = "Total electricity consumption:\n{:.2f} kWh\n\n".format(electricity_used)
    boundaries = block_tariff_data[0]
    costs = block_tariff_data[1]

    lies_in_block = bisect.bisect_right(
        boundaries, electricity_used
    )  # Determine which boundary the electricity used lies in

    # Determine the costs for all blocks except final one
    for i in range(0, lies_in_block - 1):
        amount_used = boundaries[i + 1] - 1 - boundaries[i]
        if i != 0:
            amount_used += 1
        cost_for_amount = costs[i]
        cost = amount_used * (cost_for_amount / 100.0)
        total += cost
        output += "[{}] {:.2f} kWh @ {}c/kWh = R{:.2f}\n".format(
            i + 1, amount_used, cost_for_amount, cost
        )

    # Determine final block cost
    amount_used = electricity_used - boundaries[lies_in_block - 1] + 1
    cost_for_amount = costs[lies_in_block - 1]
    cost = amount_used * (cost_for_amount / 100.0)
    total += cost
    output += "[{}] {:.2f} kWh @ {}c/kWh = R{:.2f}\n".format(
        lies_in_block, amount_used, cost_for_amount, cost
    )

    output += "\nTOTAL:\nR{:.2f}".format(total)

    return output
