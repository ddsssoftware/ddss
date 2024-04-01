<label for="{{ $fld }}">{{ $label }}</label>
<input id="{{ $fld }}" name="{{ $fld }}" value="{{ old($fld, (isset($obj) && $obj != null) ? $obj->$fld : '') }}">