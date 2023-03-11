<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use DateTime;

use App\Models\PanelLog;

class ApiController extends Controller
{
    public function dump(Request $request){
        foreach ($request->all() as $key => $log) {
            foreach ($log as $value) {
                $t = microtime(true);
                $micro = sprintf("%06d",($t - floor($t)) * 1000000);
                $d = new DateTime( date('Y-m-d H:i:s.'.$micro, $t) );

                $date = $d->format("Y-m-d H:i:s.u");
                $data = [
                    'idPanel' => $key,
                    'date' => $date,
                    ...$value['log']
                ];
                $log = new PanelLog($data);

                try{
                    $log->save();
                }catch(\Exception $e){
                    return response()->json(['error' => 'An error ocurred trying to dump the data']);
                }
            }
        }
        return response()->json(['success' => 'Datae dumped successfully!']);
    }

    public function historic(Request $request){
        $from = $request->input('from');
        $to = $request->input('to');
        $panelId = $request->input('id');

        $logs = PanelLog::where('idPanel', $panelId)->where('date', '>=', $from)->where('date', '<=', $to)->get();
        return response()->json($logs);
    }
}
