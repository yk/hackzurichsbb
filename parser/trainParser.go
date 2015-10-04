package main

import (
	"bufio"
	"os"
	"strings"
)

func main() {
	file, err := os.Open("trainInfo.in")
	if(err != nil) {
		panic(err)
	}
	defer file.Close()

	outFile, err := os.Create("trainInfo.out")
	if err != nil {
		panic(err)
	}
	defer outFile.Close()

	scanner := bufio.NewScanner(file)

	for scanner.Scan() {
		line := scanner.Text()

		split := strings.Split(line, " ")
		start := len(split[0])

		index := strings.Index(line, "full")
		if index == -1 {
			index = strings.Index(line, "assisted")
		}

		if index == -1 {
			index = strings.Index(line, "restricted")
		}

		if index != -1 {
			outFile.WriteString(line[0:start] + " " + line[index:len(line)] + "\n")
		}
//		split := strings.Split(line, " ")
//		if strings.Contains(split[0], "+") {
//			nr := strings.Split(split[0], "+")
//			for i := 0; i < len(nr); i++ {
//				outFile.WriteString(nr[i] + line[len(split[0]):len(line)] + "\n")
//			}
//		} else if strings.Contains(split[0], "-") {
//			nr := strings.Split(split[0], "-")
//			start, err := strconv.Atoi(nr[0])
//			if err != nil {
//				panic(err)
//			}

//			end, err := strconv.Atoi(nr[1])
//			if err != nil {
//				panic(err)
//			}

//			for ; start <= end; start++ {
//				outFile.WriteString(strconv.Itoa(start) + line[len(split[0]):len(line)] + "\n")
//			}
//		} else {
//			outFile.WriteString(line + "\n")
//		}
	}
}
