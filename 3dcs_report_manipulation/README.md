# 3dcs_report_manipulation
3DCS Report manupulation

Does:
 - Removes any results with the tag  [VAL] for validation measurements or  [SUB] for sub measurements
 - Reformats any line with the tag [HEADER] to be a sub header in the result list, recommended is to add the measurement as an empty dll measurement.
 - Calculates a limit based on (sigma_limit * std), sigma_limit is set to 5 to account for the limits to be +/- 5 sigma, this is displayed in the report under "Parent" for lack of something better


ToDo:
 - Would be good to be able to specify a folder sometimes and not always use the latest created, need some additional consideration 
 - Add sigma tag to be able to use different sigma levels on different measurements
