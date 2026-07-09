true = True
false = False

def propagateTree(nested_data, target_data, within_target_branch=False):
    """
    Recursively searches through a nested data structure (list or dictionary) for a specific target value.
    When the target value is found, the function returns the related path and modifies the 'expanded' property
    in the corresponding branch to True.

    Args:
        nested_data (list or dict): The nested data structure to search through.
        target_data (str): The target value to search for within the 'url' key of dictionaries.
        within_target_branch (bool): A flag indicating if the search is within the branch containing the target data.

    Returns:
        str or None: The path related to the target data if found, otherwise None.
    """

    # Check if the current level of nested_data is a list
    if isinstance(nested_data, list):
        found_path = None  # Variable to store the found path if target_data is found

        # Iterate over each item in the list
        for i, item in enumerate(nested_data):
            # Recursively call propagateTree to search in the current item
            path = propagateTree(item, target_data, within_target_branch)

            if path:
                # If a path is found, set the 'expanded' property to True in the current item
                if "expanded" in item:
                    item["expanded"] = True
                found_path = path
            else:
                # If no path is found and the current item is a dictionary with 'expanded', set it to False
                if isinstance(item, dict) and "expanded" in item:
                    item["expanded"] = False

        return found_path  # Return the found path (if any) or None

    # Check if the current level of nested_data is a dictionary
    elif isinstance(nested_data, dict):
        # If the 'url' key matches the target_data, set 'expanded' to True and return the 'path'
        if nested_data.get("url") == target_data:
            if "expanded" in nested_data:
                nested_data["expanded"] = True
            within_target_branch = True  # Update the flag to indicate we are within the target branch
            return nested_data.get("path")

        found_path = None  # Variable to store the found path if target_data is found

        # Iterate over each key-value pair in the dictionary
        for key, value in nested_data.items():
            # Recursively call propagateTree to search in the current value
            path = propagateTree(value, target_data, within_target_branch)

            if path:
                # If a path is found, set the 'expanded' property to True in the current dictionary
                if "expanded" in nested_data:
                    nested_data["expanded"] = True
                found_path = path
            elif not within_target_branch:
                # If no path is found and we are not within the target branch, set 'expanded' to False
                if isinstance(value, dict) and "expanded" in value:
                    value["expanded"] = False

        return found_path  # Return the found path (if any) or None

    # If nested_data is neither a list nor a dictionary, return None
    return None


tree_data = [
  {
    "label": "Clarios",
    "expanded": true,
    "data": {
      "path": "0",
      "url": ""
    },
    "items": [
      {
        "label": "Pacifico",
        "expanded": true,
        "data": {
          "path": "0/0",
          "url": ""
        },
        "items": [
          {
            "label": "Administracion",
            "expanded": false,
            "data": {
              "path": "0/0/0",
              "url": ""
            },
            "items": [
              {
                "label": "Modelo",
                "expanded": false,
                "data": {
                  "path": "0/0/0/0",
                  "url": "/relations"
                },
                "items": []
              },
              {
                "label": "Nodos",
                "expanded": false,
                "data": {
                  "path": "0/0/0/1",
                  "url": "/node"
                },
                "items": []
              }
            ]
          },
          {
            "label": "Tapas y cubiertas",
            "expanded": false,
            "data": {
              "path": "0/0/1",
              "url": ""
            },
            "items": [

				{
				"label": "IMM 15",
				"expanded": false,
				"data": {
				  "path": "0/0/1/0",
				  "url": "/imm/4/overview"
				},
				"items": [
					{
					"label": "OEE",
					"expanded": false,
					"data": {
					  "path": "0/0/1/0/0",
					  "url": "/imm/4/OEE"
					},
					"items": []
					},
					{
					"label": "Agendamiento",
					"expanded": false,
					"data": {
					  "path": "0/0/1/0/1",
					  "url": "/imm/4/wo"
					},
					"items": []
					},
					{
					"label": "Control de corridas",
					"expanded": false,
					"data": {
					  "path": "0/0/1/0/2",
					  "url": "/imm/4/run"
					},
					"items": []
					},
					{
					"label": "Disponibilidad",
					"expanded": false,
					"data": {
					  "path": "0/0/1/0/3",
					  "url": "/imm/4/availability"
					},
					"items": []
					},
					{
					"label": "Analisis de rendimiento",
					"expanded": false,
					"data": {
					  "path": "0/0/1/0/4",
					  "url": "/imm/4/performance"
					},
					"items": []
					},
					{
					"label": "Analisis de disponibilidad",
					"expanded": false,
					"data": {
					  "path": "0/0/1/0/5",
					  "url": "/imm/4/analysis"
					},
					"items": []
					}
				
				]
				},

				{
				"label": "Asignacion de razones",
				"expanded": false,
				"data": {
				  "path": "0/0/1/1",
				  "url": "/reason"
				},
				"items": []
				},
				{
				"label": "Gestion de eventos",
				"expanded": false,
				"data": {
				  "path": "0/0/1/2",
				  "url": "/manage"
				},
				"items": []
				}
        
        
            ]
          },
          {
            "label": "Alarmas",
            "expanded": false,
            "data": {
              "path": "0/0/2",
              "url": "/alarms"
            },
            "items": []
          }
          
          
        ]
      }
    ]
  }
]

tree_data_op = [ 
  {
    "label": "Clarios",
    "expanded": true,
    "data": {
      "path": "0",
      "url": ""
    },
    "items": [
      {
        "label": "Pacifico",
        "expanded": true,
        "data": {
          "path": "0/0",
          "url": ""
        },
        "items": [
          {
            "label": "Tapas y cubiertas",
            "expanded": false,
            "data": {
              "path": "0/0/1",
              "url": ""
            },
            "items": [

              {
                "label": "IMM 15",
                "expanded": false,
                "data": {
                  "path": "0/0/1/0",
                  "url": "/imm/4/overview"
                },
                "items": [
                  {
                    "label": "OEE",
                    "expanded": false,
                    "data": {
                      "path": "0/0/1/0/0",
                      "url": "/imm/4/OEE"
                    },
                    "items": []
                  },
                  {
                    "label": "Control de corridas",
                    "expanded": false,
                    "data": {
                      "path": "0/0/1/0/2",
                      "url": "/imm/4/run"
                    },
                    "items": []
                  }
                ]
              },

              {
                "label": "Asignacion de razones",
                "expanded": false,
                "data": {
                  "path": "0/0/1/1",
                  "url": "/reason"
                },
                "items": []
              },
              {
                "label": "Gestion de eventos",
                "expanded": false,
                "data": {
                  "path": "0/0/1/2",
                  "url": "/manage"
                },
                "items": []
              }
            ]
          },
          {
            "label": "Alarmas",
            "expanded": false,
            "data": {
              "path": "0/0/2",
              "url": "/alarms"
            },
            "items": []
          }
        ]
      }
    ]
  }
]