import json

## Method 1) From Python dictionary
x = {
    "account": "GBCXF42Q26WFS2KJ5XDM5KGOWR5M4GHR3DBTFBJVRYKRUYJK4DBIH3RX",
    "created": 1443745594,
    "creator": "GBEZOC5U4TVH7ZY5N3FLYHTCZSI6VFGTULG7PBITLF5ZEBPJXFT46YZM",
    "deleted": False,
    "payments": 44,
    "trades": 0,
    "activity": {
        "yearly": "zero",
        "monthly": "zero"
    }
}

# adding item to dict
x["children"] = []


## Method 2) From JSON string
x1 = """{
	 "activity": {
       "yearly": "zero",
       "monthly": "zero"
     }
}"""

# Convert from JSON string to Python dictionary:
y1 = json.loads(x1)

# adding item to dict
y1["children"] = []


# the result is a Python dictionary:
print(x)
print(y1)


# ====== 
issuers_dict = {}

issuers_dict['ABCD'] = {
    "account": "GBCXF42Q26WFS2KJ5XDM5KGOWR5M4GHR3DBTFBJVRYKRUYJK4DBLOBST",
    "created": 1443745594,
    "creator": "GBEZOC5U4TVH7ZY5N3FLYHTCZSI6VFGTULG7PBITLF5ZEBPJXFT46YZM",
    "deleted": False,
    "payments": 32,
    "trades": 0,
    "activity": {
        "yearly": "zero",
        "monthly": "zero"
    }
}

issuers_dict['QRST'] = {
    "account": "GBCXF42Q26WFS2KJ5XDM5KGOWR5M4GHR3DBTFBJVRYKRUYJK4DBIH3RX",
    "created": 1443745594,
    "creator": "GBEZOC5U4TVH7ZY5N3FLYHTCZSI6VFGTULG7PBITLF5ZEBPJXFT46YZM",
    "deleted": False,
    "payments": 44,
    "trades": 0,
    "activity": {
        "yearly": "zero",
        "monthly": "zero"
    }
}

print(issuers_dict)
print(issuers_dict['QRST'])
print(json.dumps(issuers_dict['QRST']))
print(json.dumps(issuers_dict))


issuer_test_dict = {
	"ISSUER_0": {
		"account": "GD6WU64OEP5C4LRBH6NK3MHYIA2ADN6K6II6EXPNVUR3ERBXT4AN4ACD",
		"created": 1446506817,
		"creator": "GBCXF42Q26WFS2KJ5XDM5KGOWR5M4GHR3DBTFBJVRYKRUYJK4DBIH3RX",
		"deleted": False,
		"payments": 170922,
		"trades": 0,
		"activity": {
			"yearly": "zero",
			"monthly": "zero"
		}
	},
	"ISSUER_1": {
		"account": "GBCXF42Q26WFS2KJ5XDM5KGOWR5M4GHR3DBTFBJVRYKRUYJK4DBIH3RX",
		"created": 1443745594,
		"creator": "GBEZOC5U4TVH7ZY5N3FLYHTCZSI6VFGTULG7PBITLF5ZEBPJXFT46YZM",
		"deleted": False,
		"payments": 44,
		"trades": 0,
		"activity": {
			"yearly": "zero",
			"monthly": "zero"
		}
	},
	"ISSUER_2": {
		"account": "GBEZOC5U4TVH7ZY5N3FLYHTCZSI6VFGTULG7PBITLF5ZEBPJXFT46YZM",
		"created": 1443672901,
		"creator": "GALPCCZN4YXA3YMJHKL6CVIECKPLJJCTVMSNYWBTKJW4K5HQLYLDMZTB",
		"deleted": False,
		"payments": 20,
		"trades": 0,
		"activity": {
			"yearly": "low",
			"monthly": "zero"
		}
	},
	"ISSUER_3": {
		"account": "GALPCCZN4YXA3YMJHKL6CVIECKPLJJCTVMSNYWBTKJW4K5HQLYLDMZTB",
		"created": 1443633354,
		"creator": "GAAZI4TCR3TY5OJHCTJC2A4QSY6CJWJH5IAJTGKIN2ER7LBNVKOCCWN7",
		"deleted": False,
		"payments": 16,
		"trades": 0,
		"activity": {
			"yearly": "zero",
			"monthly": "zero"
		}
	},
	"ISSUER_4": {
		"account": "GAAZI4TCR3TY5OJHCTJC2A4QSY6CJWJH5IAJTGKIN2ER7LBNVKOCCWN7",
		"created": "",
		"creator": "",
		"deleted": False,
		"payments": 3,
		"trades": 0,
		"activity": {
			"yearly": "zero",
			"monthly": "zero"
		}
	}
}


print(issuer_test_dict['ISSUER_2'])

issuer_test_dict['ISSUER_2']['node_type'] = "ISSUER"

print(json.dumps(issuer_test_dict))

