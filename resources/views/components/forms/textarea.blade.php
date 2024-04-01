<label for="{{ $fld }}">{{ $label }}</label>
<textarea name="{{ $fld }}">{{ old($fld, (isset($obj) && $obj != null) ? $obj->$fld :  '') }}</textarea>