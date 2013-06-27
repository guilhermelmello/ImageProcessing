function [im]=imgReadGrayScale(img)
	im = imgGrayScale(imread(img));
endfunction

function [im]=imgGhost(img, borderLength)
	[m n] = size(img);
	im = zeros(m+borderLength*2, n+borderLength*2);
	im(1+borderLength:m+borderLength, 1+borderLength:n+borderLength) = img;
endfunction

function [pixel]=pixelConvolution(window, mask)
	pixel = sum(window.*mask);
endfunction

function [im]=imgConvolution(img, mask)
	[m n] = size(img);
	borderLength = int(size(mask, 1)/2);
	im = zeros(m+borderLength*2, n+borderLength*2);
	for i = 1+borderLength:m-borderLength
		for j = 1+borderLength:n-borderLength
			im(i, j) = pixelConvolution(img(i-borderLength:i+borderLength, j-borderLength:j+borderLength), mask);
		end
	end
endfunction

function [im]=imgNeighborhood(img, mask)
	[m n] = size(img);
	maskSize = size(mask, 1)*size(mask, 2);
	im = imgConvolution(img, mask)/maskSize;
	borderLength = int(size(mask, 1)/2);
	im = im(1+borderLength:m-borderLength, 1+borderLength:n-borderLength);
endfunction

function [im]=imgKNeighbors(img, neighborhood, k)
	[m n] = size(img);
	half = int(neighborhood/2);
	im = zeros(img);
	max = neighborhood*neighborhood-1;
	min = max-k+1;
	for i = 1+half:m-half
		for j = 1+half:n-half
			neighbors = img(i-half:i+half, j-half:j+half);
			neighbors = neighbors(:);
			[x y] = sort(abs(neighbors - img(i, j)));
			im(i, j) = sum(neighbors(y(min:max)))/k;
		end
	end
	im = im(1+half:m-half, 1+half:n-half);
endfunction

function [im]=imgMedian(img, neighborhood)
	[m n] = size(img);
	half = int(neighborhood/2);
	im = zeros(img);
	center = int((neighborhood*neighborhood)/2);
	for i = 1+half:m-half
		for j = 1+half:n-half
			neighbors = img(i-half:i+half, j-half:j+half);
			neighbors = neighbors(:);
			neighbors = sort(neighbors);
			im(i, j) = neighbors(center);
		end
	end
	im = im(1+half:m-half, 1+half:n-half);
endfunction

function [im]=imgRoberts(img, mask)	
	[m n] = size(img);
	borderLength = int(size(mask, 1)/2);
	maskTwo(:, 1) = mask(:, 2);
	maskTwo(:, 2) = mask(:, 1);
	for i = 1:m-borderLength
		for j = 1:n-borderLength
			im(i, j) = pixelConvolution(img(i:i+1, j:j+1), mask) + pixelConvolution(img(i:i+1, j:j+1), maskTwo)
		end
	end
endfunction

function [im]=imgPrewitt(img, mask)
	im = imgConvolution(img, mask)+imgConvolution(img, mask);
endfunction

function [im]=imgSobel(img, mask)
	im = imgConvolution(img, mask)+imgConvolution(img, mask);
endfunction

function [im]=imgLaplace(img, mask)
	im = imgConvolution(img, mask);
endfunction

stacksize(80000000);

maskRoberts = [1 0; 0 -1];
maskPrewitt = [-1 -1 -1; 0 0 0; 1 1 1];
maskSobel = [-1 -2 -1; 0 0 0; 1 2 1];
maskLaplace = [0 -1 0; -1 4 -1; 0 -1 0];
maskNeighbor = [[1 1 1]; [1 1 1]; [1 1 1]];

image = 'D:\cg\atividade2\imagens\lena';
img = gray_imread(image+".tif");

borderLength = int(size(maskNeighbor, 1)/2);
img = imgGhost(img, borderLength);

imwrite(imgNeighborhood(img, maskNeighbor), image+"_neighborhood.png");
imwrite(imgKNeighbors(img, 9, 80), image+"_kneighbors.png");
imwrite(imgMedian(img, 15), image+"_median.png");
//imwrite(imgLaplace(img, maskLaplace),image+"_laplace.png");
//imwrite(imgRoberts(img, maskRoberts), image+"_roberts.png");
//imwrite(imgPrewitt(img, maskPrewitt), image+"_prewitt.png");
//imwrite(imgSobel(img, maskSobel), image+"_sobel.png");