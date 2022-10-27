#!/bin/bash
package_path=/home/pi/Desktop/run/pi-camera-iris/
LED_duration=$1
LED_intervention=$2
repeat_n=$3
recording_file_path=$4

delay_percent=0.4
video_duration0=`echo $LED_duration $LED_intervention $repeat_n \
	| awk '{print ($1 + $2) * 2 * $3 }'`
video_duration=`echo $video_duration0 $delay_percent | awk '{print $1 + $1 * $2}'`
recording_script=${package_path}/utils/recording.py
led_control_script=${package_path}/utils/LED_control.py
$recording_script $recording_file_path $video_duration&
$led_control_script $LED_duration $LED_intervention $repeat_n&
