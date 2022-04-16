package main

import (
	"fmt"
	"os/exec"
	"strings"
)

func main() {
	cmd := "ps aux | grep  worker_scheduler/main | grep -v grep "
	out, err := exec.Command("bash", "-c", cmd).Output()
	if err != nil {
		fmt.Println("Failed to execute command:", cmd)
	}
	fmt.Println(string(out))
	v := strings.Split(string(out), "\n")
	fmt.Println(v)

}




// hello.go

package main

import (
        "sync"
		"os/exec"
        "fmt"
)

var wg sync.WaitGroup

func main() {

        arr:= []int{1166801,1350788,1579342,1358650}
        for _, value := range arr {
                wg.Add(1)
                //cmd := "python ./pr_scope_close_2.py --prs " , value , " --id _devpublish --branch 21.2R3 --product junos "

				cmd := fmt.Sprintf("python ./pr_scope_close_2.py --prs %d --id _devpublish --branch 21.2R3 --product junos ", value)
                go func() {
                   fmt.Println(cmd)
				   out, err := exec.Command("bash", "-c", cmd).Output()
				   if err != nil {
					   fmt.Println("Failed to execute command:", cmd)
				   }
				   fmt.Println(string(out))
                   wg.Done()
                }()
        }
        wg.Wait()
}